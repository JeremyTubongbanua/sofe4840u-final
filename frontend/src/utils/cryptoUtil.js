const sign = async (challengeString, privateKeyBase64) => {
    try {
        const privateKeyBytes = Uint8Array.from(atob(privateKeyBase64), c => c.charCodeAt(0));
        
        let privateKey;
        try {
            privateKey = await window.crypto.subtle.importKey(
                "pkcs8",
                privateKeyBytes,
                {
                    name: "RSA-PSS",
                    hash: { name: "SHA-256" },
                },
                false,
                ["sign"]
            );
        } catch (pkcs8Error) {
            try {
                privateKey = await window.crypto.subtle.importKey(
                    "spki",
                    privateKeyBytes,
                    {
                        name: "RSA-PSS",
                        hash: { name: "SHA-256" },
                    },
                    false,
                    ["sign"]
                );
            } catch (spkiError) {
                try {
                    const pemContent = privateKeyBase64
                        .replace(/-----(BEGIN|END) (PRIVATE KEY|RSA PRIVATE KEY)-----/g, "")
                        .replace(/\s/g, "");
                    const pemBytes = Uint8Array.from(atob(pemContent), c => c.charCodeAt(0));
                    
                    privateKey = await window.crypto.subtle.importKey(
                        "pkcs8",
                        pemBytes,
                        {
                            name: "RSA-PSS",
                            hash: { name: "SHA-256" },
                        },
                        false,
                        ["sign"]
                    );
                } catch (pemError) {
                    throw new Error("Failed to import private key in any supported format");
                }
            }
        }

        const challengeBytes = new TextEncoder().encode(challengeString);

        const signature = await window.crypto.subtle.sign(
            {
                name: "RSA-PSS",
                saltLength: 32,
            },
            privateKey,
            challengeBytes
        );

        const signatureBase64 = btoa(String.fromCharCode.apply(null, new Uint8Array(signature)));
        return signatureBase64;
        
    } catch (error) {
        console.error("Error signing challenge:", error);
        throw new Error(`Failed to sign challenge: ${error.message}`);
    }
};

export { sign };