/**
 * TypeScript type definitions for authentication.
 * These types match the Pydantic schemas in backend/app/schemas/auth.py
 */

/**
 * User registration request payload
 */
export interface UserRegister {
  email: string;
  password: string; // Minimum 8 characters
}

/**
 * User login request payload
 */
export interface UserLogin {
  email: string;
  password: string;
}

/**
 * User response (after registration or login)
 */
export interface UserResponse {
  user_id: string;
  email: string;
  token: string;
}

/**
 * Decoded token data
 */
export interface TokenData {
  user_id: string | null;
}
