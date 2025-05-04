"use client";

import { useDeviceDetection } from "@/hooks/useDeviceDetection";
import MobileView from "@/components/custom/MobileView";
import { inter } from "@/fonts/Inter";

type Children = {
  children: React.ReactNode
}

const DesktopBody = ( { children }: Children ) => {

    const { isDesktop } = useDeviceDetection();

    return (
        <body className={`${inter.variable} antialiased`}>
            { isDesktop ? children : <MobileView/>}
        </body>
    );
};

export default DesktopBody;
