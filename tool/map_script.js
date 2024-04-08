// map_script.js
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // alert("Node ID " + text + " copied to clipboard!");
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
}
