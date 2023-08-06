// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

use std::fmt::Display;
use std::io;
use std::pin::Pin;
use std::task::ready;
use std::task::Context;
use std::task::Poll;

use bytes::Bytes;
use futures::future::BoxFuture;
use futures::AsyncWrite;
use futures::FutureExt;

use crate::raw::oio::Write;
use crate::raw::*;
use crate::*;

/// Writer is designed to write data into given path in an asynchronous
/// manner.
///
/// ## Notes
///
/// Please make sure either `close` or `abort` has been called before
/// dropping the writer otherwise the data could be lost.
///
/// ## Notes
///
/// Writer can be used in two ways:
///
/// - Sized: write data with a known size by specify the content length.
/// - Unsized: write data with an unknown size, also known as streaming.
///
/// All services will support `sized` writer and provide special optimization if
/// the given data size is the same as the content length, allowing them to
/// be written in one request.
///
/// Some services also supports `unsized` writer. They MAY buffer part of the data
/// and flush them into storage at needs. And finally, the file will be available
/// after `close` has been called.
pub struct Writer {
    state: State,
}

/// # Safety
///
/// Writer will only be accessed by `&mut Self`
unsafe impl Sync for Writer {}

impl Writer {
    /// Create a new writer.
    ///
    /// Create will use internal information to decide the most suitable
    /// implementation for users.
    ///
    /// We don't want to expose those details to users so keep this function
    /// in crate only.
    pub(crate) async fn create(acc: FusedAccessor, path: &str, op: OpWrite) -> Result<Self> {
        let (_, w) = acc.write(path, op).await?;

        Ok(Writer {
            state: State::Idle(Some(w)),
        })
    }

    /// Write into inner writer.
    pub async fn write(&mut self, bs: impl Into<Bytes>) -> Result<()> {
        if let State::Idle(Some(w)) = &mut self.state {
            w.write(bs.into()).await
        } else {
            unreachable!(
                "writer state invalid while write, expect Idle, actual {}",
                self.state
            );
        }
    }

    /// Abort the writer and clean up all written data.
    ///
    /// ## Notes
    ///
    /// Abort should only be called when the writer is not closed or
    /// aborted, otherwise an unexpected error could be returned.
    pub async fn abort(&mut self) -> Result<()> {
        if let State::Idle(Some(w)) = &mut self.state {
            w.abort().await
        } else {
            unreachable!(
                "writer state invalid while abort, expect Idle, actual {}",
                self.state
            );
        }
    }

    /// Close the writer and make sure all data have been committed.
    ///
    /// ## Notes
    ///
    /// Close should only be called when the writer is not closed or
    /// aborted, otherwise an unexpected error could be returned.
    pub async fn close(&mut self) -> Result<()> {
        if let State::Idle(Some(w)) = &mut self.state {
            w.close().await
        } else {
            unreachable!(
                "writer state invalid while close, expect Idle, actual {}",
                self.state
            );
        }
    }
}

enum State {
    Idle(Option<oio::Writer>),
    Write(BoxFuture<'static, Result<(usize, oio::Writer)>>),
    Close(BoxFuture<'static, Result<oio::Writer>>),
}

impl Display for State {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            State::Idle(_) => write!(f, "Idle"),
            State::Write(_) => write!(f, "Write"),
            State::Close(_) => write!(f, "Close"),
        }
    }
}

impl AsyncWrite for Writer {
    fn poll_write(
        mut self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &[u8],
    ) -> Poll<io::Result<usize>> {
        loop {
            match &mut self.state {
                State::Idle(w) => {
                    let mut w = w
                        .take()
                        .expect("invalid state of writer: Idle state with empty write");
                    let bs = Bytes::from(buf.to_vec());
                    let size = bs.len();
                    let fut = async move {
                        w.write(bs).await?;
                        Ok((size, w))
                    };
                    self.state = State::Write(Box::pin(fut));
                }
                State::Write(fut) => match ready!(fut.poll_unpin(cx)) {
                    Ok((size, w)) => {
                        self.state = State::Idle(Some(w));
                        return Poll::Ready(Ok(size));
                    }
                    Err(err) => return Poll::Ready(Err(io::Error::new(io::ErrorKind::Other, err))),
                },
                State::Close(_) => {
                    unreachable!("invalid state of writer: poll_write with State::Close")
                }
            };
        }
    }

    /// Writer makes sure that every write is flushed.
    fn poll_flush(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<io::Result<()>> {
        Poll::Ready(Ok(()))
    }

    fn poll_close(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>> {
        loop {
            match &mut self.state {
                State::Idle(w) => {
                    let mut w = w
                        .take()
                        .expect("invalid state of writer: Idle state with empty write");
                    let fut = async move {
                        w.close().await?;
                        Ok(w)
                    };
                    self.state = State::Close(Box::pin(fut));
                }
                State::Write(_) => {
                    unreachable!("invalid state of writer: poll_close with State::Write")
                }
                State::Close(fut) => match ready!(fut.poll_unpin(cx)) {
                    Ok(w) => {
                        self.state = State::Idle(Some(w));
                        return Poll::Ready(Ok(()));
                    }
                    Err(err) => return Poll::Ready(Err(io::Error::new(io::ErrorKind::Other, err))),
                },
            }
        }
    }
}

impl tokio::io::AsyncWrite for Writer {
    fn poll_write(
        mut self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &[u8],
    ) -> Poll<io::Result<usize>> {
        loop {
            match &mut self.state {
                State::Idle(w) => {
                    let mut w = w
                        .take()
                        .expect("invalid state of writer: Idle state with empty write");
                    let bs = Bytes::from(buf.to_vec());
                    let size = bs.len();
                    let fut = async move {
                        w.write(bs).await?;
                        Ok((size, w))
                    };
                    self.state = State::Write(Box::pin(fut));
                }
                State::Write(fut) => match ready!(fut.poll_unpin(cx)) {
                    Ok((size, w)) => {
                        self.state = State::Idle(Some(w));
                        return Poll::Ready(Ok(size));
                    }
                    Err(err) => return Poll::Ready(Err(io::Error::new(io::ErrorKind::Other, err))),
                },
                State::Close(_) => {
                    unreachable!("invalid state of writer: poll_write with State::Close")
                }
            };
        }
    }

    fn poll_flush(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<io::Result<()>> {
        Poll::Ready(Ok(()))
    }

    fn poll_shutdown(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<io::Result<()>> {
        loop {
            match &mut self.state {
                State::Idle(w) => {
                    let mut w = w
                        .take()
                        .expect("invalid state of writer: Idle state with empty write");
                    let fut = async move {
                        w.close().await?;
                        Ok(w)
                    };
                    self.state = State::Close(Box::pin(fut));
                }
                State::Write(_) => {
                    unreachable!("invalid state of writer: poll_close with State::Write")
                }
                State::Close(fut) => match ready!(fut.poll_unpin(cx)) {
                    Ok(w) => {
                        self.state = State::Idle(Some(w));
                        return Poll::Ready(Ok(()));
                    }
                    Err(err) => return Poll::Ready(Err(io::Error::new(io::ErrorKind::Other, err))),
                },
            }
        }
    }
}

/// BlockingWriter is designed to write data into given path in an blocking
/// manner.
pub struct BlockingWriter {
    pub(crate) inner: oio::BlockingWriter,
}

impl BlockingWriter {
    /// Create a new writer.
    ///
    /// Create will use internal information to decide the most suitable
    /// implementation for users.
    ///
    /// We don't want to expose those details to users so keep this function
    /// in crate only.
    pub(crate) fn create(acc: FusedAccessor, path: &str, op: OpWrite) -> Result<Self> {
        let (_, w) = acc.blocking_write(path, op)?;

        Ok(BlockingWriter { inner: w })
    }

    /// Write into inner writer.
    pub fn write(&mut self, bs: impl Into<Bytes>) -> Result<()> {
        self.inner.write(bs.into())
    }

    /// Close the writer and make sure all data have been stored.
    pub fn close(&mut self) -> Result<()> {
        self.inner.close()
    }
}

impl io::Write for BlockingWriter {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        let size = buf.len();
        self.inner
            .write(Bytes::from(buf.to_vec()))
            .map(|_| size)
            .map_err(|err| io::Error::new(io::ErrorKind::Other, err))
    }

    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}
