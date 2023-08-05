use std::str::FromStr;

use pyo3::prelude::*;
use rand::seq::SliceRandom;
use rand::Rng;
use serde::de::{self, Deserializer, MapAccess, SeqAccess, Visitor};
use serde::ser::{SerializeStruct, Serializer};
use serde::{Deserialize, Serialize};

use crate::signal_type::generators::*;
use crate::signal_type::*;

#[pyclass]
#[derive(Debug)]
pub struct SignalGenerator {
    pub inner: Box<dyn Signal>,
}

#[pyfunction]
pub const fn get_max_limit() -> f64 {
    i32::MAX as f64
}

#[pyfunction]
pub const fn get_min_limit() -> f64 {
    i32::MIN as f64
}

fn calculate_minimum_and_maximum(
    is_signed: bool,
    num_bits: u8,
    scale: f64,
    offset: f64,
) -> (f64, f64) {
    let (lvalue, rvalue) = {
        if is_signed {
            let min_by_bits = 1i64 << (num_bits - 1);
            let lvalue = -1.0 * scale * min_by_bits as f64 + offset;
            // avoid overflow in the following function
            let max_by_bits = (1i64 << (num_bits - 1)) - 1;
            let rvalue = scale * max_by_bits as f64 + offset;
            (lvalue, rvalue)
        } else {
            let lvalue = offset;
            let max_by_bits = (1 << num_bits) - 1;
            let rvalue = scale * max_by_bits as f64 + offset;
            (lvalue, rvalue)
        }
    };

    if lvalue > rvalue {
        (rvalue, lvalue)
    } else {
        (lvalue, rvalue)
    }
}

#[pymethods]
impl SignalGenerator {
    #[new]
    #[pyo3(signature = (
        *,
        signal_type,
        minimum = get_min_limit(),
        maximum = get_max_limit(),
        amplitude,
        period,
        phase,
        num_bits,
        is_signed,
        scale,
        offset
    ))]
    pub fn new(
        signal_type: SignalType,
        mut minimum: f64,
        mut maximum: f64,
        amplitude: f64,
        period: f64,
        phase: f64,
        num_bits: u8,
        is_signed: bool,
        scale: f64,
        offset: f64,
    ) -> Self {
        if minimum > maximum {
            panic!("Minimum must be less than or equal to maximum");
        }

        if minimum == get_min_limit() && maximum == get_max_limit() {
            (minimum, maximum) = calculate_minimum_and_maximum(is_signed, num_bits, scale, offset);
        } else if minimum == get_min_limit() {
            minimum = calculate_minimum_and_maximum(is_signed, num_bits, scale, offset).0;
        } else if maximum == get_max_limit() {
            maximum = calculate_minimum_and_maximum(is_signed, num_bits, scale, offset).1;
        }

        let inner: Box<dyn Signal> = match signal_type {
            SignalType::Sine => Box::new(Sine {
                minimum,
                maximum,
                amplitude,
                period,
                phase,
                num_bits,
                is_signed,
                scale,
                offset,
            }),
            SignalType::Square => Box::new(Square {
                minimum,
                maximum,
                amplitude,
                period,
                phase,
                num_bits,
                is_signed,
                scale,
                offset,
            }),
            SignalType::Triangle => Box::new(Triangle {
                minimum,
                maximum,
                amplitude,
                period,
                phase,
                num_bits,
                is_signed,
                scale,
                offset,
            }),
            SignalType::Sawtooth => Box::new(Sawtooth {
                minimum,
                maximum,
                amplitude,
                period,
                phase,
                num_bits,
                is_signed,
                scale,
                offset,
            }),
            SignalType::Constant => Box::new(Constant {
                minimum,
                maximum,
                amplitude,
                period,
                phase,
                num_bits,
                is_signed,
                scale,
                offset,
            }),
        };
        SignalGenerator { inner }
    }

    pub fn calculate(&self, time: f64) -> i64 {
        self.inner.calculate(time)
    }

    pub fn to_json(&self) -> String {
        serde_json::to_string(self).unwrap()
    }

    #[staticmethod]
    #[pyo3(
        signature = (
            num_bits,
            is_signed,
            scale,
            offset,
            /,
            *,
            minimum = get_min_limit(),
            maximum = get_max_limit()
        )
    )]
    pub fn default_constant_signal(
        num_bits: u8,
        is_signed: bool,
        scale: f64,
        offset: f64,
        minimum: f64,
        maximum: f64,
    ) -> Self {
        SignalGenerator::new(
            SignalType::Constant,
            minimum,
            maximum,
            0.0,
            0.0,
            0.0,
            num_bits,
            is_signed,
            scale,
            offset,
        )
    }

    /// Generate a random signal with the given parameters
    #[staticmethod]
    #[pyo3(
        signature = (
            num_bits,
            is_signed,
            scale,
            offset,
            /,
            *,
            minimum = get_min_limit(),
            maximum = get_max_limit()
        )
    )]
    pub fn random_signal(
        num_bits: u8,
        is_signed: bool,
        scale: f64,
        offset: f64,
        minimum: f64,
        maximum: f64,
    ) -> Self {
        // Randomly choose a signal type
        let mut rng = rand::thread_rng();
        let signal_type = SignalType::get_types().choose(&mut rng).unwrap().clone();
        let amplitude = rng.gen_range(0.0..100.0);
        let period = rng.gen_range(0.0..10.0);
        let phase = rng.gen_range(0.0..period);

        SignalGenerator::new(
            signal_type,
            minimum,
            maximum,
            amplitude,
            period,
            phase,
            num_bits,
            is_signed,
            scale,
            offset,
        )
    }

    /// Turns a JSON string into a SignalGenerator
    ///
    /// # Arguments
    /// * `json` - A JSON string representing a SignalGenerator
    ///
    /// # Returns
    /// A SignalGenerator
    #[staticmethod]
    pub fn from_json(json: &str) -> Self {
        serde_json::from_str(json).unwrap()
    }
}

/// Allow SignalGenerator to be compared for equality
impl PartialEq for SignalGenerator {
    fn eq(&self, other: &Self) -> bool {
        // Compare all params
        self.inner.get_type() == other.inner.get_type()
            && self.inner.get_minimum() == other.inner.get_minimum()
            && self.inner.get_maximum() == other.inner.get_maximum()
            && self.inner.get_amplitude() == other.inner.get_amplitude()
            && self.inner.get_period() == other.inner.get_period()
            && self.inner.get_phase() == other.inner.get_phase()
            && self.inner.get_num_bits() == other.inner.get_num_bits()
            && self.inner.is_signed() == other.inner.is_signed()
            && self.inner.get_scale() == other.inner.get_scale()
            && self.inner.get_offset() == other.inner.get_offset()
    }
}

/// Allow SignalGenerator to be Serializeable
///
/// This allows a way to store a certain configuration for a Signal in a file and load it later
///
/// # Example Structure
/// ```json
/// {
///    "type": "Sine",
///    "amplitude": 1.0,
///    "frequency": 440.0,
///    "phase": 0.0
///    "num_bits": 16,
///    "is_signed": false,
///    "scale": 1.0,
///    "offset": 0.0
/// }
/// ```
impl Serialize for SignalGenerator {
    /// Serialize the `SignalGenerator` to a Serde-compatible format
    ///
    /// # Arguments
    ///
    /// * `serializer` - The serializer to use
    ///
    /// # Returns
    ///
    /// A Result containing the serialized `SignalGenerator` if successful, or an error if not
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let inner = self.inner.as_ref();
        let mut state = serializer.serialize_struct("SignalGenerator", 10)?;
        state.serialize_field("type", &inner.get_type_name())?;
        state.serialize_field("minimum", &inner.get_minimum())?;
        state.serialize_field("maximum", &inner.get_maximum())?;
        state.serialize_field("amplitude", &inner.get_amplitude())?;
        state.serialize_field("period", &inner.get_period())?;
        state.serialize_field("phase", &inner.get_phase())?;
        state.serialize_field("num_bits", &inner.get_num_bits())?;
        state.serialize_field("is_signed", &inner.is_signed())?;
        state.serialize_field("scale", &inner.get_scale())?;
        state.serialize_field("offset", &inner.get_offset())?;
        state.end()
    }
}

/// Allow SignalGenerator to be Deserializeable
///
/// This allows a way to load a certain configuration for a Signal from a file
impl<'de> Deserialize<'de> for SignalGenerator {
    /// Deserialize the `SignalGenerator` from a Serde-compatible format
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        /// The fields in the JSON file
        #[derive(Deserialize)]
        #[serde(field_identifier, rename_all = "lowercase")]
        enum Field {
            Type,
            Minimum,
            Maximum,
            Amplitude,
            Period,
            Phase,
            #[serde(rename = "num_bits")]
            NumBits,
            #[serde(rename = "is_signed")]
            IsSigned,
            Scale,
            Offset,
        }

        /// The visitor that will walk through the JSON file
        struct SignalGeneratorVisitor;

        /// The visitor implementation
        impl<'de> Visitor<'de> for SignalGeneratorVisitor {
            /// The type we want to deserialize
            type Value = SignalGenerator;

            fn expecting(&self, formatter: &mut std::fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("struct SignalGenerator")
            }

            fn visit_seq<V>(self, mut seq: V) -> Result<Self::Value, V::Error>
            where
                V: SeqAccess<'de>,
            {
                let signal_type: SignalType = SignalType::from_str(
                    seq.next_element()?
                        .ok_or_else(|| de::Error::invalid_length(0, &self))?,
                )
                .expect("Invalid signal type");

                let minimum: f64 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(1, &self))?;

                let maximum: f64 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(2, &self))?;

                let amplitude: f64 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(3, &self))?;

                let period: f64 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(4, &self))?;

                let phase: f64 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(5, &self))?;

                let num_bits: u8 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(6, &self))?;

                let is_signed: bool = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(7, &self))?;

                let scale: f64 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(8, &self))?;

                let offset: f64 = seq
                    .next_element()?
                    .ok_or_else(|| de::Error::invalid_length(9, &self))?;

                Ok(SignalGenerator::new(
                    signal_type,
                    minimum,
                    maximum,
                    amplitude,
                    period,
                    phase,
                    num_bits,
                    is_signed,
                    scale,
                    offset,
                ))
            }

            fn visit_map<V>(self, mut map: V) -> Result<SignalGenerator, V::Error>
            where
                V: MapAccess<'de>,
            {
                let mut signal_type: Option<SignalType> = None;
                let mut minimum: Option<f64> = None;
                let mut maximum: Option<f64> = None;
                let mut amplitude: Option<f64> = None;
                let mut period: Option<f64> = None;
                let mut phase: Option<f64> = None;
                let mut num_bits: Option<u8> = None;
                let mut is_signed: Option<bool> = None;
                let mut scale: Option<f64> = None;
                let mut offset: Option<f64> = None;

                // Deserialize the fields in any order
                while let Some(key) = map.next_key()? {
                    match key {
                        Field::Type => {
                            if signal_type.is_some() {
                                return Err(de::Error::duplicate_field("type"));
                            }

                            let parse_signal_type = SignalType::from_str(
                                Some(map.next_value()?).expect("You need to specify a signal type"),
                            );

                            // If the signal type is invalid / not parsable
                            if !parse_signal_type.is_ok() {
                                return Err(de::Error::custom("Invalid signal type"));
                            }

                            signal_type = parse_signal_type.ok();
                        }
                        Field::Minimum => {
                            if minimum.is_some() {
                                return Err(de::Error::duplicate_field("minimum"));
                            }
                            minimum = Some(map.next_value()?);
                        }
                        Field::Maximum => {
                            if maximum.is_some() {
                                return Err(de::Error::duplicate_field("maximum"));
                            }
                            maximum = Some(map.next_value()?);
                        }
                        Field::Amplitude => {
                            if amplitude.is_some() {
                                return Err(de::Error::duplicate_field("amplitude"));
                            }
                            amplitude = Some(map.next_value()?);
                        }
                        Field::Period => {
                            if period.is_some() {
                                return Err(de::Error::duplicate_field("period"));
                            }
                            period = Some(map.next_value()?);
                        }
                        Field::Phase => {
                            if phase.is_some() {
                                return Err(de::Error::duplicate_field("phase"));
                            }
                            phase = Some(map.next_value()?);
                        }
                        Field::NumBits => {
                            if num_bits.is_some() {
                                return Err(de::Error::duplicate_field("num_bits"));
                            }
                            num_bits = Some(map.next_value()?);
                        }
                        Field::IsSigned => {
                            if is_signed.is_some() {
                                return Err(de::Error::duplicate_field("is_signed"));
                            }
                            is_signed = Some(map.next_value()?);
                        }
                        Field::Scale => {
                            if scale.is_some() {
                                return Err(de::Error::duplicate_field("scale"));
                            }
                            scale = Some(map.next_value()?);
                        }
                        Field::Offset => {
                            if offset.is_some() {
                                return Err(de::Error::duplicate_field("offset"));
                            }
                            offset = Some(map.next_value()?);
                        }
                    }
                }

                let signal_type = signal_type.ok_or_else(|| de::Error::missing_field("type"))?;
                let minimum = minimum.ok_or_else(|| de::Error::missing_field("minimum"))?;
                let maximum = maximum.ok_or_else(|| de::Error::missing_field("maximum"))?;
                let amplitude = amplitude.ok_or_else(|| de::Error::missing_field("amplitude"))?;
                let period = period.ok_or_else(|| de::Error::missing_field("period"))?;
                let phase = phase.ok_or_else(|| de::Error::missing_field("phase"))?;
                let num_bits = num_bits.ok_or_else(|| de::Error::missing_field("num_bits"))?;
                let is_signed = is_signed.ok_or_else(|| de::Error::missing_field("is_signed"))?;
                let scale = scale.ok_or_else(|| de::Error::missing_field("scale"))?;
                let offset = offset.ok_or_else(|| de::Error::missing_field("offset"))?;

                Ok(SignalGenerator::new(
                    signal_type,
                    minimum,
                    maximum,
                    amplitude,
                    period,
                    phase,
                    num_bits,
                    is_signed,
                    scale,
                    offset,
                ))
            }
        }

        const FIELDS: &'static [&'static str] = &[
            "type",
            "minimum",
            "maximum",
            "amplitude",
            "period",
            "phase",
            "num_bits",
            "is_signed",
            "scale",
            "offset",
        ];

        deserializer.deserialize_struct("SignalGenerator", FIELDS, SignalGeneratorVisitor)
    }
}

#[cfg(test)]
mod generation_tests {
    use super::*;

    #[test]
    fn test_default_generation() {
        let num_bits = 32;
        let is_signed = true;
        let scale = 1.0;
        let offset = 0.0;

        let minimum = get_min_limit();
        let maximum = get_max_limit();

        let default_signal = SignalGenerator::default_constant_signal(
            num_bits, is_signed, scale, offset, minimum, maximum,
        );

        assert_eq!(default_signal.inner.get_type(), SignalType::Constant);
        assert_eq!(default_signal.inner.get_num_bits(), num_bits);
        assert_eq!(default_signal.inner.is_signed(), is_signed);
        assert_eq!(default_signal.inner.get_scale(), scale);
        assert_eq!(default_signal.inner.get_offset(), offset);
    }

    #[test]
    fn test_random_generation() {
        let num_bits = 32;
        let is_signed = true;
        let scale = 1.0;
        let offset = 0.0;

        let minimum = get_min_limit();
        let maximum = get_max_limit();

        let _random_signal =
            SignalGenerator::random_signal(num_bits, is_signed, scale, offset, minimum, maximum);

        assert!(true);
    }

    #[test]
    fn test_more_random_generation() {
        let num_bits = 16;
        let is_signed = false;
        let scale = 0.0001;
        let offset = 0.0;

        let minimum = get_min_limit();
        let maximum = get_max_limit();

        let random_signal =
            SignalGenerator::random_signal(num_bits, is_signed, scale, offset, minimum, maximum);

        let mut rng = rand::thread_rng();
        for _i in 0..100 {
            let value = random_signal.calculate(rng.gen_range(0.0..1000.0));
            assert!(value as f64 / scale >= 0.0);
            assert!(value as f64 / scale <= 65535.0);
        }
    }
}

#[cfg(test)]
mod serialization_tests {
    use std::f64::consts::PI;

    use super::{SignalGenerator, SignalType};
    use rand::prelude::*;
    use serde_test::{assert_tokens, Token};

    /// Macro to test serialization and deserialization for a given type
    macro_rules! test_ser_de {
        ($name:ident) => {
            /// Test serialization and deserialization for a given type
            #[test]
            #[allow(non_snake_case)]
            fn $name() {
                for _i in 0..100 {
                    let mut rng = rand::thread_rng();
                    // Full Test
                    {
                        let min = super::get_min_limit();
                        let max = super::get_max_limit();
                        let amp = rng.gen::<f64>();
                        let period = rng.gen::<f64>();
                        let phase = rng.gen::<f64>();
                        let num_bits: u8 = rng.gen_range(1u8..16u8);
                        let is_signed = rng.gen::<bool>();
                        let scale: f64 = rng.gen_range(-1.0f64..10.0f64);
                        let offset: f64 = rng.gen_range(-100.0f64..100.0f64);

                        // minimum, maximum based on signed or unsigned and number of bits and offset and scale
                        let (calculated_min, calculated_max) = super::calculate_minimum_and_maximum(
                            is_signed, num_bits, scale, offset,
                        );

                        let signal = SignalGenerator::new(
                            SignalType::$name,
                            min,
                            max,
                            amp,
                            period,
                            phase,
                            num_bits,
                            is_signed,
                            scale,
                            offset,
                        );

                        assert_tokens(
                            &signal,
                            &[
                                Token::Struct {
                                    name: "SignalGenerator",
                                    len: 10,
                                },
                                Token::String("type"),
                                Token::BorrowedStr(stringify!($name)),
                                Token::String("minimum"),
                                Token::F64(calculated_min),
                                Token::String("maximum"),
                                Token::F64(calculated_max),
                                Token::String("amplitude"),
                                Token::F64(amp),
                                Token::String("period"),
                                Token::F64(period),
                                Token::String("phase"),
                                Token::F64(phase),
                                Token::String("num_bits"),
                                Token::U8(num_bits),
                                Token::String("is_signed"),
                                Token::Bool(is_signed),
                                Token::String("scale"),
                                Token::F64(scale),
                                Token::String("offset"),
                                Token::F64(offset),
                                Token::StructEnd,
                            ],
                        )
                    }
                }
            }
        };
    }

    #[test]
    fn serialize_sin_demo() {
        let amp: f64 = 12.0;
        let min: f64 = 0.0;
        let max: f64 = 101.0;
        let period: f64 = PI;
        let phase: f64 = 0.0;
        let num_bits: u8 = 16;
        let is_signed: bool = true;
        let scale: f64 = 1.0;
        let offset: f64 = 0.0;

        let signal = SignalGenerator::new(
            SignalType::Sine,
            min,
            max,
            amp,
            period,
            phase,
            num_bits,
            is_signed,
            scale,
            offset,
        );
        assert_tokens(
            &signal,
            &[
                Token::Struct {
                    name: "SignalGenerator",
                    len: 10,
                },
                Token::String("type"),
                Token::BorrowedStr("Sine"),
                Token::String("minimum"),
                Token::F64(min),
                Token::String("maximum"),
                Token::F64(max),
                Token::String("amplitude"),
                Token::F64(amp),
                Token::String("period"),
                Token::F64(period),
                Token::String("phase"),
                Token::F64(phase),
                Token::String("num_bits"),
                Token::U8(num_bits),
                Token::String("is_signed"),
                Token::Bool(is_signed),
                Token::String("scale"),
                Token::F64(scale),
                Token::String("offset"),
                Token::F64(offset),
                Token::StructEnd,
            ],
        )
    }

    test_ser_de!(Sine);
    test_ser_de!(Square);
    test_ser_de!(Triangle);
    test_ser_de!(Sawtooth);
    test_ser_de!(Constant);
}
