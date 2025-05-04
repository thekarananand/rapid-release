import type { Metadata } from "next";
import "./globals.css";
import DesktopBody from "@/components/custom/DesktopBody";

export const metadata: Metadata = {
    title: "Rapid Release",
    description: "Manage All DevOps Stuff in one place",
};

type Children = {
    children: React.ReactNode
}

export default function RootLayout( { children }: Children ) {
    return (
        <html lang="en">
            <DesktopBody>
                {children}
            </DesktopBody>
        </html>
    );
}
