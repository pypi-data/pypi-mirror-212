use std::str::FromStr;

use pyo3::prelude::*;

use strum::IntoEnumIterator;
use strum_macros::{Display, EnumIter, EnumString};

/// The different signals that can be generated
#[pyclass]
#[derive(Copy, Clone, Display, EnumIter, EnumString, PartialEq, Debug)]
pub enum SignalType {
    Sine,
    Square,
    Triangle,
    Sawtooth,
    Constant,
}

#[pymethods]
impl SignalType {
    pub fn to_string(&self) -> &'static str {
        match self {
            SignalType::Sine => "Sine",
            SignalType::Square => "Square",
            SignalType::Triangle => "Triangle",
            SignalType::Sawtooth => "Sawtooth",
            SignalType::Constant => "Constant",
        }
    }

    #[staticmethod]
    pub fn parse(string: &str) -> Self {
        SignalType::from_str(string).unwrap()
    }

    #[staticmethod]
    pub fn from(string: &str) -> Self {
        SignalType::from_str(string).unwrap()
    }

    #[staticmethod]
    pub fn from_string(string: &str) -> Self {
        SignalType::from_str(string).unwrap()
    }

    #[staticmethod]
    pub fn get_types() -> Vec<SignalType> {
        SignalType::iter().collect()
    }

    fn __repr__(&self) -> &'static str {
        self.to_string()
    }
}

pub mod generators {
    use super::SignalType;

    use core::fmt::Debug;
    use rand::Rng;
    use std::f64::consts::PI;

    /// A macro to create structs for each SignalType with the fields: amplitude, frequency, phase (all f64)
    macro_rules! signal_type_struct {
        ($($name:ident),*) => {
            $(
                #[derive(Debug)]
                pub struct $name {
                    pub minimum: f64,
                    pub maximum: f64,
                    pub amplitude: f64,
                    pub period: f64,
                    pub phase: f64,
                    pub num_bits: u8,
                    pub is_signed: bool,
                    pub scale: f64,
                    pub offset: f64
                }
            )*
        };
    }

    macro_rules! signal_type_getters {
        ($name:ident) => {
            fn get_type(&self) -> SignalType {
                SignalType::$name
            }
            fn get_minimum(&self) -> f64 {
                self.minimum
            }
            fn get_maximum(&self) -> f64 {
                self.maximum
            }
            fn get_amplitude(&self) -> f64 {
                self.amplitude
            }
            fn get_period(&self) -> f64 {
                self.period
            }
            fn get_phase(&self) -> f64 {
                self.phase
            }
            fn get_num_bits(&self) -> u8 {
                self.num_bits
            }
            fn is_signed(&self) -> bool {
                self.is_signed
            }
            fn get_scale(&self) -> f64 {
                self.scale
            }
            fn get_offset(&self) -> f64 {
                self.offset
            }
        };
    }

    // Create structs for each SignalType
    signal_type_struct!(Sine, Square, Triangle, Sawtooth, Constant);

    pub trait Signal: Send {
        fn get_type(&self) -> SignalType;
        fn get_minimum(&self) -> f64;
        fn get_maximum(&self) -> f64;
        fn get_amplitude(&self) -> f64;
        fn get_period(&self) -> f64;
        fn get_phase(&self) -> f64;
        fn get_num_bits(&self) -> u8;
        fn is_signed(&self) -> bool;
        fn get_scale(&self) -> f64;
        fn get_offset(&self) -> f64;

        fn get_type_name(&self) -> &'static str {
            self.get_type().to_string()
        }

        /// Shrink a value to only take up a certain number of bits
        /// after the scale and offset have been applied
        ///
        /// Note: the number has to remain within the range of the signal's
        /// minimum and maximum values
        fn shrink_to_fit(&self, value: f64) -> i64 {
            // Apply the reverse of the scale and offset
            let clamped = value.max(self.get_minimum()).min(self.get_maximum());
            let scale_factor = {
                if self.get_scale() < 1.0 {
                    self.get_scale()
                } else {
                    1.0
                }
            };
            let scaled = clamped / scale_factor;
            let offset = scaled - self.get_offset();
            let offset = offset.round() as i64;

            let num_bits = self.get_num_bits();
            let is_signed = self.is_signed();

            let max_value = if is_signed {
                2_i64.pow(num_bits as u32 - 1) - 1
            } else {
                2_i64.pow(num_bits as u32) - 1
            };

            let min_value = if is_signed {
                -(2_i64.pow(num_bits as u32 - 1))
            } else {
                0
            };

            // Clamp the value to the range of the number of bits
            let clamped = offset.max(min_value).min(max_value);

            // Undo the scale and offset
            let clamped = (clamped as f64 + self.get_offset()) * scale_factor;
            let rounded = clamped.round() as i64;

            if rounded as f64 > self.get_maximum() {
                self.get_maximum() as i64
            } else if self.get_minimum() > rounded as f64 {
                self.get_minimum() as i64
            } else {
                rounded
            }
        }

        /// Calculates the fraction to use as the noise
        fn noise(&self) -> f64 {
            static NOISE: f64 = 0.01;
            let mut rng = rand::thread_rng();
            rng.gen_range(-NOISE..NOISE)
        }

        /// Calculate the value of the signal at a given time with noise
        fn calculate(&self, time: f64) -> i64;
    }

    impl Debug for dyn Signal {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            f.debug_struct("Signal")
                .field("type", &self.get_type_name())
                .field("minimum", &self.get_minimum())
                .field("maximum", &self.get_maximum())
                .field("amplitude", &self.get_amplitude())
                .field("period", &self.get_period())
                .field("phase", &self.get_phase())
                .field("num_bits", &self.get_num_bits())
                .field("is_signed", &self.is_signed())
                .field("scale", &self.get_scale())
                .field("offset", &self.get_offset())
                .finish()
        }
    }

    impl Signal for Sine {
        signal_type_getters!(Sine);

        fn calculate(&self, time: f64) -> i64 {
            let a = self.get_amplitude();
            let b = 2.0 * PI / self.get_period();
            let c = self.get_phase();

            let value = a * ((b * (time + c)).sin() + self.noise());
            let value = value.clamp(self.minimum, self.maximum);
            self.shrink_to_fit(value)
        }
    }

    impl Signal for Square {
        signal_type_getters!(Square);

        fn calculate(&self, time: f64) -> i64 {
            let value = {
                if (time + self.phase) % self.period < self.period / 2.0 {
                    self.amplitude
                } else {
                    -self.amplitude
                }
            };
            let value = value + self.noise() * self.get_amplitude();
            let value = value.clamp(self.minimum, self.maximum);
            self.shrink_to_fit(value)
        }
    }

    impl Signal for Triangle {
        signal_type_getters!(Triangle);

        fn calculate(&self, time: f64) -> i64 {
            let t = (time + self.phase) % self.period / self.period;
            let value = {
                if t < 0.25 {
                    self.amplitude * t * 4.0
                } else if t < 0.75 {
                    self.amplitude * (1.0 - (t - 0.25) * 4.0)
                } else {
                    self.amplitude * (t - 0.75) * 4.0 - self.amplitude
                }
            };
            let value = value + self.noise() * self.amplitude;
            let value = value.clamp(self.minimum, self.maximum);
            self.shrink_to_fit(value)
        }
    }

    impl Signal for Sawtooth {
        signal_type_getters!(Sawtooth);

        fn calculate(&self, time: f64) -> i64 {
            let t: f64 = (time + self.phase) % self.period / self.period;
            let value = self.amplitude * (t * 2.0 - 1.0);
            let value = value + self.noise() * self.amplitude;
            let value = value.clamp(self.minimum, self.maximum);
            self.shrink_to_fit(value)
        }
    }

    impl Signal for Constant {
        signal_type_getters!(Constant);

        fn calculate(&self, _time: f64) -> i64 {
            let value = self.amplitude;
            let value = value + self.noise() * self.amplitude;
            let value = value.clamp(self.minimum, self.maximum);
            self.shrink_to_fit(value)
        }
    }
}

#[cfg(test)]
mod signal_test {
    use crate::{
        signal_generator::{get_max_limit, get_min_limit},
        signal_type::generators::Signal,
    };

    #[test]
    fn sine_test() {
        use super::*;

        let signal_type = SignalType::Constant;
        let minimum = get_min_limit();
        let maximum = get_max_limit();
        let amplitude = 8200.0;
        let period = 100.0;
        let phase = 0.0;
        let num_bits: u8 = 16;
        let is_signed = true;
        let scale = 100.0;
        let offset = 0.0;

        let signal = generators::Constant {
            minimum,
            maximum,
            amplitude,
            period,
            phase,
            num_bits,
            is_signed,
            scale,
            offset,
        };

        dbg!(signal.calculate(0.0));
    }
}
