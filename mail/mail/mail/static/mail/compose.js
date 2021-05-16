/*
document.addEventListener('DOMContentLoaded',
    function ()
    {
        const form = document.querySelector("#compose-form");
        const message = document.querySelector("#message");
        form.addEventListener("submit", (event) => {
        to = document.querySelector("#compose-recipients").value;
        subject = document.querySelector("#compose-subject").value;
        body = document.querySelector("#compose-body").value;
        if (to.length == 0) return;

        fetch("/emails", 
        {
            method: "POST",
            body: JSON.stringify
            ({
            recipients: to,
            subject: subject,
            body: body,
            }),
        })
        .catch((error) =>
        { 
            console.log(error);
        })
        .then((response) => 
        {
            if (!response.ok)
            {
                return Promise.reject('api call failed');
            }
            response.json()
            //response.json())
        })
        .then((result) => {
            console.log(result.status);
        });
    }
);
*/
document.addEventListener('DOMContentLoaded',
    function ()
    {
        const form = document.querySelector("#compose-form");
        const message = document.querySelector("#message");
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            to = document.querySelector("#compose-recipients").value;
            subject = document.querySelector("#compose-subject").value;
            body = document.querySelector("#compose-body").value;
            fetch("/emails", 
            {
                method: "POST",
                body: JSON.stringify
                ({
                recipients: to,
                subject: subject,
                body: body,
                }),
            })
            .then((response) => {
                if (!response.ok){
                    return Promise.reject('api call failed');
                }
                return response.json;
            })
            .catch((error) =>
            { 
                console.log(response);
                console.log(error);
            })
        });
    },
    false
);