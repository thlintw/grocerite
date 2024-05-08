<script lang="ts">
    import Button from "$lib/components/Button.svelte";
    import { Html5Qrcode } from "html5-qrcode";
    import { onMount, onDestroy, createEventDispatcher } from "svelte";
    import jsQR from "jsqr";

    let reader: HTMLElement;
    let html5QrCode: Html5Qrcode;

    onMount(() => {
        html5QrCode = new Html5Qrcode(reader.id);
        // html5QrCode.start(
        // cameraId, 
        // {
        //     fps: 10,    // Optional, frame per seconds for qr code scanning
        //     qrbox: { width: 250, height: 250 }  // Optional, if you want bounded box UI
        // },
        // (decodedText, decodedResult) => {
        //     // do something when code is read
        // },
        // (errorMessage) => {
        //     // parse error, ignore it.
        // })
        // .catch((err) => {
        // // Start failed, handle it.
        // });
        const qrCodeSuccessCallback = (decodedText, decodedResult) => {
            console.log('success', decodedText, decodedResult);
            html5QrCode.pause(true);
        };

        const qrCodeFailureCallback = (decodedText, decodedResult) => {
            /* handle failure */
        };
        const config = { fps: 10, qrbox: { width: 250, height: 250 } };
        html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback, qrCodeFailureCallback);
    });

    onDestroy(() => {
        if (html5QrCode) {
            html5QrCode.stop().then(() => {
                // QR Code scanning is stopped.
            }).catch((err) => {
                // Stop failed, handle it.
            });

        }
    });

    const dispatch = createEventDispatcher();

    const onUpload = () => {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.onchange = async (event) => {
            let imgFile: File;
            if (fileInput.files && fileInput.files.length > 0) {
                imgFile = fileInput.files[0];
                const reader = new FileReader();
                reader.onload = (e) => {
                    if (e.target) {
                        const imageData = e.target.result as string;
                        const image = new Image();
                        image.onload = () => {
                            const canvas = document.createElement('canvas');
                            const context = canvas.getContext('2d');
                            canvas.width = image.width;
                            canvas.height = image.height;
                            context!.drawImage(image, 0, 0);
                            const imageData = context!.getImageData(0, 0, canvas.width, canvas.height);
                            const code = jsQR(
                                imageData.data,
                                imageData.width,
                                imageData.height, 
                                {
                                    inversionAttempts: "dontInvert",
                                }
                            );
                            if (code) {
                                console.log('code', code);
                            } 
                        };

                        image.src = imageData;

                        reader.readAsDataURL(imgFile);
                    }
                }
            }
        };

        fileInput.click();
    }


</script>

<div class="h-full w-full flex items-center flex-col gap-5">
    <div class="">
        Scan from other member's QR code
    </div>
    <div class="w-[600px] min-h-[450px] relative">
        <div class="absolute top-0 left-0 w-full h-full bg-black/50 flex items-center justify-center text-white">
            camera loading...
        </div>
        <div id="reader" class="w-[600px]" bind:this={reader}></div>
    </div>
    <div class="">
        Or read from image
    </div>
    <Button
        text="Upload"
        on:click={onUpload}
        />
</div>