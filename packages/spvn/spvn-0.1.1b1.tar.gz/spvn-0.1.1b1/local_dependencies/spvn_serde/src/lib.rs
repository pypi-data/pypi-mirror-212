pub mod asgi_scope;
pub mod asgi_sender;
pub mod body_receiver;
pub mod call_async;
pub mod coalesced;
pub mod event_receiver;
pub mod event_sender;
pub mod implementation;
pub mod state;

use std::collections::HashMap;

use asgi_scope::ASGIEvent;
use bytes::Bytes;

use pyo3::{
    exceptions::*,
    prelude::*,
    types::{PyBytes, PyDict},
};
use tracing::{log::warn};

/// Implementation per
/// [specification](https://asgi.readthedocs.io/en/latest/specs/www.html)
///
/// **ASGIv2.3**
#[derive(Eq, Debug, Clone, PartialEq, PartialOrd, Ord)]
pub enum ASGIType {
    /// Anon lifespan event managed by the application
    Lifespan,

    /// Lifecycle evts
    LifecycleStartup,
    LifecycleShutdown,
    LifecycleStartupSuccess,
    LifecycleStartupFailure,
    LifecycleShutdownSuccess,
    LifecycleShutdownFailure,

    /// http events
    HTTPResponseStart,
    HTTPResponseBody,
    HTTPResponseTrailers,
    HTTPDisconnect,

    // TODO: websockets homework
    WS,
}

impl ASGIType {
    pub fn from(value: String) -> Result<Self, ()> {
        let s = value.to_lowercase();
        let ma = match s.as_str() {
            // 2.2
            "lifespan" => ASGIType::Lifespan,

            "lifespan.startup.complete" => ASGIType::LifecycleStartupSuccess,
            "lifespan.startup.failed" => ASGIType::LifecycleStartupFailure,

            "lifespan.shutdown.complete" => ASGIType::LifecycleShutdownSuccess,
            "lifespan.shutdown.failed" => ASGIType::LifecycleShutdownFailure,

            "http.response.start" => ASGIType::HTTPResponseStart,
            "http.response.body" => ASGIType::HTTPResponseBody,
            "http.response.trailers" => ASGIType::HTTPResponseTrailers,

            "http.disconnect" => ASGIType::HTTPDisconnect,

            // all other messages can get out of here
            _ => return Err(()),
        };

        Ok(ma)
    }
}

impl Into<&str> for ASGIType {
    fn into(self) -> &'static str {
        match self {
            ASGIType::Lifespan => "lifespan",
            ASGIType::LifecycleStartup => "lifespan.startup",
            ASGIType::LifecycleShutdown => "lifespan.shutdown",
            ASGIType::LifecycleStartupSuccess => "lifespan.startup.success",
            ASGIType::LifecycleStartupFailure => "lifespan.startup.failure",
            ASGIType::LifecycleShutdownSuccess => "lifespan.shutdown.success",
            ASGIType::LifecycleShutdownFailure => "lifespan.shutdown.failure",
            ASGIType::HTTPResponseStart => "http.response.start",
            ASGIType::HTTPResponseBody => "http.response.body",
            ASGIType::HTTPResponseTrailers => "http.response.trailers",
            ASGIType::HTTPDisconnect => "http.disconnect",

            // TODO: websockets
            ASGIType::WS => "websocket",
        }
    }
}

impl Into<String> for ASGIType {
    fn into(self) -> String {
        let s: &'static str = self.into();
        String::from(s)
    }
}

/// Simple struct to pass the invalidation into python
pub struct InvalidationRationale {
    pub message: String,
}

impl std::convert::From<InvalidationRationale> for PyErr {
    fn from(err: InvalidationRationale) -> PyErr {
        PyValueError::new_err(err.message.to_string())
    }
}

/// Implementation per
/// [specification](https://asgi.readthedocs.io/en/latest/specs/www.html)
///
/// **ASGIv2.3**
#[derive(Debug, Clone, PartialEq, PartialOrd, Eq, Ord)]
pub struct ASGIResponse {
    _type: ASGIType,
    body: Option<Bytes>,
    headers: Vec<(String, Bytes)>,
    status: Option<u16>,
    more_body: Option<bool>,
    trailers: Option<bool>,
}

impl<'a> AsgiDict<'a> {
    fn extract_type(&self) -> Result<ASGIType, InvalidationRationale> {
        let _type = self.0.get_item("type");
        if _type.is_none() {
            #[cfg(debug_assertions)]
            {
                warn!("type provided is none")
            }
            return Err(InvalidationRationale {
                message: String::from(r#"missing "type" field"#),
            });
        };

        let _type: String = _type.unwrap().extract().expect("type must be provided");

        let _type = match ASGIType::from(_type) {
            Ok(typ) => typ,
            Err(_) => {
                #[cfg(debug_assertions)]
                {
                    warn!("invalid asgi type provided {:#?}", self)
                }
                return Err(InvalidationRationale {
                    message: String::from("invalid asgi type provided"),
                });
            }
        };
        Ok(_type)
    }
}

#[derive(Debug)]
struct AsgiDict<'a>(&'a PyDict);

impl<'a> TryInto<ASGIEvent> for AsgiDict<'a> {
    type Error = InvalidationRationale;

    fn try_into(self) -> Result<ASGIEvent, Self::Error> {
        let _type = match self.extract_type() {
            Ok(typ) => typ,
            Err(_) => {
                #[cfg(debug_assertions)]
                {
                    warn!("invalid asgi type provided {:#?}", self)
                }
                return Err(InvalidationRationale {
                    message: String::from("invalid asgi type provided"),
                });
            }
        };
        let mut message: Option<String> = None;
        let _msg = self.0.get_item("message");
        if _msg.is_some() {
            let st: Result<String, PyErr> = _msg.unwrap().extract();
            match st {
                Ok(msg) => {
                    message = Some(msg);
                }
                Err(_) => (),
            };
        }
        let state: Option<HashMap<String, String>> = None;

        // let _state = self.0.get_item("state");
        // if _state.is_some() {
        //     let st: Result<HashMap<String, String>, PyErr> = _msg.unwrap().extract();
        //     match st {
        //         Ok(msg) => {
        //             state = Some(msg);
        //         }
        //         Err(_) => (),
        //     };
        // }

        Ok(ASGIEvent {
            _type,
            message,
            state,
        })
    }
}
impl<'a> TryInto<ASGIResponse> for AsgiDict<'a> {
    type Error = InvalidationRationale;

    fn try_into(self) -> Result<ASGIResponse, Self::Error> {
        let _type = match self.extract_type() {
            Ok(typ) => typ,
            Err(_) => {
                #[cfg(debug_assertions)]
                {
                    warn!("invalid asgi type provided {:#?}", self)
                }
                return Err(InvalidationRationale {
                    message: String::from("invalid asgi type provided"),
                });
            }
        };

        let mut body: Option<Bytes> = None;
        let mut more_body: Option<bool> = None;
        let mut trailers: Option<bool> = None;
        let mut status: Option<u16> = None;

        if _type == ASGIType::HTTPResponseBody {
            let _body = self.0.get_item("body");

            if _body.is_none() {
                #[cfg(debug_assertions)]
                {
                    warn!("no body provided")
                }
                return Err(InvalidationRationale {
                    message: String::from(r#"No body provided for "http.response.body" type"#),
                });
            }
            let bts = _body.unwrap().extract::<&[u8]>().unwrap_or(&[]);
            let v: Vec<u8> = Vec::from(bts);
            let b_sr: Bytes = Bytes::from(v);
            body = Some(b_sr);

            let more = self.0.get_item("more_body");
            if more.is_some() {
                more_body = Some(
                    more.unwrap()
                        .extract()
                        .expect("invalid type provided by more_body"),
                );
            }
        } else if _type == ASGIType::HTTPResponseStart {
            let trail = self.0.get_item("trailers");
            if trail.is_some() {
                trailers = Some(
                    trail
                        .unwrap()
                        .extract()
                        .expect("invalid type provided by trailers"),
                );
            }

            let stat = self.0.get_item("status");
            if stat.is_some() {
                status = Some(
                    stat.unwrap()
                        .extract()
                        .expect("invalid type provided by status"),
                );
            }
        };

        let mut headers: Vec<(std::string::String, Bytes)> = vec![];
        let _headers = self.0.get_item("headers");

        if _headers.is_some() {
            headers = _headers
                .unwrap()
                .extract::<Vec<(&PyBytes, &PyBytes)>>()
                .expect("invalid type for headers")
                .iter_mut()
                .map(|(key, bts)| {
                    let v = Vec::from(bts.as_bytes());
                    let b = Bytes::from(v);
                    let s = std::str::from_utf8(key.as_bytes())
                        .expect("Header keys must be UTF-8 compliant (RFC5987)");
                    (String::from(s), b)
                })
                .collect();
        }

        Ok(ASGIResponse {
            _type,
            body,
            headers,
            more_body,
            trailers,
            status,
        })
    }
}
