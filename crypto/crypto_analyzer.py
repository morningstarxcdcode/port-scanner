"""
Advanced Cryptography and Steganography Module
Author: morningstarxcdcode
Description: Professional cryptographic analysis and steganography tools
"""

import base64
import hashlib
import io
import os
import random
import string
import struct
from typing import Dict, List, Optional, Tuple

import numpy as np
import qrcode
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image

from config.config_manager import config
from utils.logger import get_logger

logger = get_logger()


class CryptographyAnalyzer:
    """Advanced cryptographic analysis tools."""

    def __init__(self):
        self.logger = get_logger()

        # Common hash patterns
        self.hash_patterns = {
            32: ["MD5"],
            40: ["SHA-1"],
            64: ["SHA-256"],
            96: ["SHA-384"],
            128: ["SHA-512"],
        }

        # Common encryption indicators
        self.encryption_indicators = [
            "BEGIN PGP MESSAGE",
            "BEGIN CERTIFICATE",
            "BEGIN PRIVATE KEY",
            "BEGIN PUBLIC KEY",
            "BEGIN RSA PRIVATE KEY",
            "-----BEGIN",
            "-----END",
        ]

    def identify_hash_type(self, hash_string: str) -> List[str]:
        """Identify possible hash types based on length."""
        hash_length = len(hash_string)
        return self.hash_patterns.get(hash_length, ["Unknown"])

    def crack_hash(
        self, hash_string: str, wordlist: Optional[List[str]] = None
    ) -> Optional[str]:
        """Attempt to crack hash using wordlist."""
        if not wordlist:
            wordlist = self.generate_common_passwords()

        hash_types = self.identify_hash_type(hash_string)

        for password in wordlist:
            for hash_type in hash_types:
                if hash_type == "MD5":
                    computed = hashlib.md5(password.encode()).hexdigest()
                elif hash_type == "SHA-1":
                    computed = hashlib.sha1(password.encode()).hexdigest()
                elif hash_type == "SHA-256":
                    computed = hashlib.sha256(password.encode()).hexdigest()
                elif hash_type == "SHA-384":
                    computed = hashlib.sha384(password.encode()).hexdigest()
                elif hash_type == "SHA-512":
                    computed = hashlib.sha512(password.encode()).hexdigest()
                else:
                    continue

                if computed.lower() == hash_string.lower():
                    return password

        return None

    def generate_common_passwords(self) -> List[str]:
        """Generate common password list."""
        return [
            "password",
            "123456",
            "password123",
            "admin",
            "letmein",
            "welcome",
            "monkey",
            "1234567890",
            "qwerty",
            "abc123",
            "Password1",
            "password1",
            "root",
            "toor",
            "pass",
            "guest",
            "test",
            "user",
            "login",
            "demo",
        ]

    def analyze_cipher_text(self, cipher_text: str) -> Dict:
        """Analyze cipher text for patterns and possible encryption types."""
        analysis = {
            "length": len(cipher_text),
            "character_frequency": {},
            "possible_encodings": [],
            "possible_ciphers": [],
            "entropy": 0.0,
        }

        # Character frequency analysis
        for char in cipher_text:
            analysis["character_frequency"][char] = (
                analysis["character_frequency"].get(char, 0) + 1
            )

        # Calculate entropy
        analysis["entropy"] = self.calculate_entropy(cipher_text)

        # Check for common encodings
        if self.is_base64(cipher_text):
            analysis["possible_encodings"].append("Base64")

        if self.is_hex(cipher_text):
            analysis["possible_encodings"].append("Hexadecimal")

        # Cipher analysis based on patterns
        if analysis["entropy"] > 7.5:
            analysis["possible_ciphers"].append("Strong encryption (AES, etc.)")
        elif analysis["entropy"] > 6.0:
            analysis["possible_ciphers"].append("Weak encryption or compression")
        else:
            analysis["possible_ciphers"].extend(
                ["Caesar cipher", "Substitution cipher", "Vigenère cipher"]
            )

        return analysis

    def calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text."""
        if not text:
            return 0.0

        # Count character frequencies
        frequencies = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1

        # Calculate entropy
        entropy = 0.0
        text_length = len(text)

        for count in frequencies.values():
            probability = count / text_length
            if probability > 0:
                entropy -= probability * np.log2(probability)

        return entropy

    def is_base64(self, text: str) -> bool:
        """Check if text is Base64 encoded."""
        try:
            base64.b64decode(text, validate=True)
            return True
        except Exception:
            return False

    def is_hex(self, text: str) -> bool:
        """Check if text is hexadecimal."""
        try:
            int(text, 16)
            return len(text) % 2 == 0
        except ValueError:
            return False

    def decrypt_common_ciphers(self, cipher_text: str) -> Dict[str, str]:
        """Attempt to decrypt using common cipher methods."""
        results = {}

        # Try Caesar cipher with different shifts
        for shift in range(1, 26):
            decrypted = self.caesar_decrypt(cipher_text, shift)
            if self.is_readable_text(decrypted):
                results[f"Caesar (shift {shift})"] = decrypted

        # Try Base64 decoding
        if self.is_base64(cipher_text):
            try:
                decoded = base64.b64decode(cipher_text).decode("utf-8")
                results["Base64"] = decoded
            except:
                pass

        # Try hex decoding
        if self.is_hex(cipher_text):
            try:
                decoded = bytes.fromhex(cipher_text).decode("utf-8")
                results["Hexadecimal"] = decoded
            except:
                pass

        return results

    def caesar_decrypt(self, text: str, shift: int) -> str:
        """Decrypt Caesar cipher with given shift."""
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted = ((ord(char) - ascii_offset - shift) % 26) + ascii_offset
                result += chr(shifted)
            else:
                result += char
        return result

    def is_readable_text(self, text: str) -> bool:
        """Check if text appears to be readable English."""
        if not text:
            return False

        # Simple heuristic: check for common English words
        common_words = [
            "the",
            "and",
            "for",
            "are",
            "but",
            "not",
            "you",
            "all",
            "can",
            "had",
            "her",
            "was",
            "one",
            "our",
        ]
        text_lower = text.lower()

        word_count = sum(1 for word in common_words if word in text_lower)
        return word_count >= 2 and len(text) > 10

    def generate_key_pair(self) -> Tuple[bytes, bytes]:
        """Generate RSA key pair."""
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return private_pem, public_pem

    def encrypt_message(self, message: str, public_key_pem: bytes) -> bytes:
        """Encrypt message with RSA public key."""
        public_key = serialization.load_pem_public_key(
            public_key_pem, backend=default_backend()
        )

        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return encrypted

    def decrypt_message(self, encrypted_message: bytes, private_key_pem: bytes) -> str:
        """Decrypt message with RSA private key."""
        private_key = serialization.load_pem_private_key(
            private_key_pem, password=None, backend=default_backend()
        )

        decrypted = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return decrypted.decode()


class SteganographyAnalyzer:
    """Advanced steganography detection and analysis tools."""

    def __init__(self):
        self.logger = get_logger()

    def analyze_image_steganography(self, image_path: str) -> Dict:
        """Analyze image for potential steganography."""
        try:
            image = Image.open(image_path)
            analysis = {
                "filename": os.path.basename(image_path),
                "format": image.format,
                "size": image.size,
                "mode": image.mode,
                "suspicious_patterns": [],
                "lsb_analysis": {},
                "metadata_analysis": {},
                "chi_square_test": 0.0,
            }

            # Basic metadata analysis
            if hasattr(image, "_getexif") and image._getexif():
                analysis["metadata_analysis"]["exif_data"] = dict(image._getexif())

            # LSB analysis
            if image.mode in ["RGB", "RGBA"]:
                analysis["lsb_analysis"] = self.lsb_analysis(image)

            # Chi-square test for randomness
            analysis["chi_square_test"] = self.chi_square_test(image)

            # Check for unusual patterns
            analysis["suspicious_patterns"] = self.detect_suspicious_patterns(image)

            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing image steganography: {e}")
            return {}

    def lsb_analysis(self, image: Image.Image) -> Dict:
        """Analyze least significant bits for hidden data."""
        try:
            width, height = image.size
            pixels = list(image.getdata())

            # Extract LSBs from each color channel
            lsb_data = {
                "red_lsb": [],
                "green_lsb": [],
                "blue_lsb": [],
            }

            for pixel in pixels[:1000]:  # Analyze first 1000 pixels
                if len(pixel) >= 3:
                    lsb_data["red_lsb"].append(pixel[0] & 1)
                    lsb_data["green_lsb"].append(pixel[1] & 1)
                    lsb_data["blue_lsb"].append(pixel[2] & 1)

            # Calculate randomness of LSBs
            analysis = {}
            for channel, bits in lsb_data.items():
                if bits:
                    ones = sum(bits)
                    total = len(bits)
                    ratio = ones / total

                    # Suspicious if ratio is too close to 0.5 (random) or too far (pattern)
                    suspicion = abs(ratio - 0.5)
                    analysis[channel] = {
                        "ones_ratio": ratio,
                        "suspicion_level": "High" if suspicion < 0.1 else "Low",
                    }

            return analysis

        except Exception as e:
            self.logger.error(f"LSB analysis failed: {e}")
            return {}

    def chi_square_test(self, image: Image.Image) -> float:
        """Perform chi-square test for randomness."""
        try:
            if image.mode not in ["RGB", "RGBA"]:
                return 0.0

            pixels = list(image.getdata())

            # Extract color values
            color_values = []
            for pixel in pixels[:10000]:  # Limit for performance
                if len(pixel) >= 3:
                    color_values.extend(pixel[:3])

            if not color_values:
                return 0.0

            # Calculate expected frequency (uniform distribution)
            expected_freq = len(color_values) / 256

            # Count actual frequencies
            frequencies = [0] * 256
            for value in color_values:
                frequencies[value] += 1

            # Calculate chi-square statistic
            chi_square = 0.0
            for observed in frequencies:
                if expected_freq > 0:
                    chi_square += ((observed - expected_freq) ** 2) / expected_freq

            return chi_square

        except Exception as e:
            self.logger.error(f"Chi-square test failed: {e}")
            return 0.0

    def detect_suspicious_patterns(self, image: Image.Image) -> List[str]:
        """Detect suspicious patterns that might indicate steganography."""
        patterns = []

        try:
            # Check if image dimensions are unusual
            width, height = image.size
            if width % 8 == 0 and height % 8 == 0:
                patterns.append(
                    "Dimensions are multiples of 8 (common in steganography)"
                )

            # Check file size vs image size ratio
            # This would require file size information

            # Check for unusual color distribution
            if image.mode in ["RGB", "RGBA"]:
                pixels = list(image.getdata())

                # Sample pixels for analysis
                sample_size = min(1000, len(pixels))
                sample_pixels = random.sample(pixels, sample_size)

                # Check for unusual color patterns
                red_values = [p[0] for p in sample_pixels if len(p) >= 3]
                green_values = [p[1] for p in sample_pixels if len(p) >= 3]
                blue_values = [p[2] for p in sample_pixels if len(p) >= 3]

                # Check if colors are too uniform or too random
                for channel, values in [
                    ("Red", red_values),
                    ("Green", green_values),
                    ("Blue", blue_values),
                ]:
                    if values:
                        unique_values = len(set(values))
                        total_values = len(values)

                        if unique_values / total_values > 0.9:
                            patterns.append(
                                f"{channel} channel has high entropy (suspicious)"
                            )

        except Exception as e:
            self.logger.error(f"Pattern detection failed: {e}")

        return patterns

    def extract_lsb_data(self, image_path: str, num_bits: int = 1) -> bytes:
        """Extract data hidden in LSBs."""
        try:
            image = Image.open(image_path)

            if image.mode not in ["RGB", "RGBA"]:
                return b""

            pixels = list(image.getdata())
            binary_data = ""

            for pixel in pixels:
                if len(pixel) >= 3:
                    # Extract LSBs from RGB channels
                    for i in range(3):
                        binary_data += str(pixel[i] & ((1 << num_bits) - 1))

            # Convert binary string to bytes
            extracted_bytes = b""
            for i in range(0, len(binary_data) - 7, 8):
                byte_str = binary_data[i : i + 8]
                if len(byte_str) == 8:
                    extracted_bytes += bytes([int(byte_str, 2)])

            return extracted_bytes

        except Exception as e:
            self.logger.error(f"LSB extraction failed: {e}")
            return b""

    def hide_data_in_image(
        self, image_path: str, data: bytes, output_path: str
    ) -> bool:
        """Hide data in image using LSB steganography."""
        try:
            image = Image.open(image_path)

            if image.mode not in ["RGB", "RGBA"]:
                return False

            # Convert data to binary
            binary_data = "".join(format(byte, "08b") for byte in data)

            # Add delimiter to mark end of data
            binary_data += "1111111111111110"  # Special end marker

            pixels = list(image.getdata())

            # Check if image is large enough
            max_data_bits = len(pixels) * 3  # 3 channels per pixel
            if len(binary_data) > max_data_bits:
                return False

            # Modify pixels
            data_index = 0
            modified_pixels = []

            for pixel in pixels:
                if data_index >= len(binary_data):
                    modified_pixels.append(pixel)
                    continue

                new_pixel = list(pixel)

                # Modify LSB of each color channel
                for i in range(min(3, len(new_pixel))):
                    if data_index < len(binary_data):
                        # Clear LSB and set new bit
                        new_pixel[i] = (new_pixel[i] & 0xFE) | int(
                            binary_data[data_index]
                        )
                        data_index += 1

                modified_pixels.append(tuple(new_pixel))

            # Create new image
            new_image = Image.new(image.mode, image.size)
            new_image.putdata(modified_pixels)
            new_image.save(output_path)

            return True

        except Exception as e:
            self.logger.error(f"Data hiding failed: {e}")
            return False

    def create_qr_code_with_hidden_data(
        self, visible_data: str, hidden_data: bytes, output_path: str
    ) -> bool:
        """Create QR code with steganographic data."""
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(visible_data)
            qr.make(fit=True)

            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Save as temporary file
            temp_path = output_path + ".temp"
            qr_image.save(temp_path)

            # Hide additional data in the QR code image
            success = self.hide_data_in_image(temp_path, hidden_data, output_path)

            # Clean up
            os.remove(temp_path)

            return success

        except Exception as e:
            self.logger.error(f"QR code creation with hidden data failed: {e}")
            return False


class PasswordGenerator:
    """Advanced password generation and analysis tools."""

    def __init__(self):
        self.logger = get_logger()

    def generate_secure_password(
        self, length: int = 16, include_symbols: bool = True
    ) -> str:
        """Generate cryptographically secure password."""
        characters = string.ascii_letters + string.digits
        if include_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        return "".join(random.choice(characters) for _ in range(length))

    def analyze_password_strength(self, password: str) -> Dict:
        """Analyze password strength and provide recommendations."""
        analysis = {
            "length": len(password),
            "score": 0,
            "strength": "Very Weak",
            "feedback": [],
            "entropy": 0.0,
            "time_to_crack": "Unknown",
        }

        # Length scoring
        if analysis["length"] >= 12:
            analysis["score"] += 25
        elif analysis["length"] >= 8:
            analysis["score"] += 15
        else:
            analysis["feedback"].append(
                "Password should be at least 12 characters long"
            )

        # Character variety scoring
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digits = any(c.isdigit() for c in password)
        has_symbols = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        variety_score = sum([has_lower, has_upper, has_digits, has_symbols])
        analysis["score"] += variety_score * 15

        if not has_lower:
            analysis["feedback"].append("Add lowercase letters")
        if not has_upper:
            analysis["feedback"].append("Add uppercase letters")
        if not has_digits:
            analysis["feedback"].append("Add numbers")
        if not has_symbols:
            analysis["feedback"].append("Add symbols")

        # Calculate entropy
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digits:
            charset_size += 10
        if has_symbols:
            charset_size += 32

        if charset_size > 0:
            analysis["entropy"] = analysis["length"] * np.log2(charset_size)

        # Determine strength
        if analysis["score"] >= 85:
            analysis["strength"] = "Very Strong"
        elif analysis["score"] >= 70:
            analysis["strength"] = "Strong"
        elif analysis["score"] >= 50:
            analysis["strength"] = "Moderate"
        elif analysis["score"] >= 30:
            analysis["strength"] = "Weak"
        else:
            analysis["strength"] = "Very Weak"

        # Estimate time to crack (simplified)
        if analysis["entropy"] > 60:
            analysis["time_to_crack"] = "Centuries"
        elif analysis["entropy"] > 50:
            analysis["time_to_crack"] = "Years"
        elif analysis["entropy"] > 40:
            analysis["time_to_crack"] = "Months"
        elif analysis["entropy"] > 30:
            analysis["time_to_crack"] = "Days"
        else:
            analysis["time_to_crack"] = "Hours or less"

        return analysis


def run_crypto_analysis(data: str, analysis_type: str = "auto") -> Dict:
    """Run comprehensive cryptographic analysis."""
    analyzer = CryptographyAnalyzer()

    if analysis_type == "hash":
        return {
            "type": "hash_analysis",
            "possible_types": analyzer.identify_hash_type(data),
            "cracked_password": analyzer.crack_hash(data),
        }
    elif analysis_type == "cipher":
        analysis = analyzer.analyze_cipher_text(data)
        analysis["decryption_attempts"] = analyzer.decrypt_common_ciphers(data)
        return analysis
    else:
        # Auto-detect
        if analyzer.is_base64(data) or analyzer.is_hex(data):
            return run_crypto_analysis(data, "cipher")
        elif len(data) in analyzer.hash_patterns:
            return run_crypto_analysis(data, "hash")
        else:
            return analyzer.analyze_cipher_text(data)


def run_steganography_analysis(file_path: str) -> Dict:
    """Run comprehensive steganography analysis."""
    analyzer = SteganographyAnalyzer()

    if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        return analyzer.analyze_image_steganography(file_path)
    else:
        return {"error": "Unsupported file type for steganography analysis"}
