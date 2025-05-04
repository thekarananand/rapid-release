import { useState, useEffect } from "react";

export function useDeviceDetection() {
    const [isDesktop, setIsDesktop] = useState<boolean>(true);

    useEffect(() => {
        const checkDevice = () => {
            setIsDesktop(window.innerWidth >= 600 && window.innerHeight >= 600);
        };
        checkDevice();
        window.addEventListener("resize", checkDevice);
        return () => window.removeEventListener("resize", checkDevice);
    }, []);

    return { isDesktop };
}
