import {jwtDecode} from 'jwt-decode';

interface DecodedToken {
    sub: string;
    account_type: string;
    exp: number;
}
export default DecodedToken;

export const decodeToken = (token: string): DecodedToken | null => {
    try {
        return jwtDecode<DecodedToken>(token);
    } catch (error) {
        console.error('Failed to decode token', error);
        return null;
    }
};

export const isTokenExpired = (token: string): boolean => {
    const decoded = decodeToken(token);
    if (!decoded) {
        return true;
    }
    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime;
};
