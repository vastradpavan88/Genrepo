
document.addEventListener(
    "DOMContentLoaded",
    function () {

        const fileInput =
            document.getElementById("file");


        if (fileInput) {

            fileInput.addEventListener(
                "change",
                function () {

                    if (
                        this.files &&
                        this.files.length > 0
                    ) {

                        console.log(
                            "Selected file: " +
                            this.files[0].name
                        );

                    }

                }
            );

        }

    }
);