const loadScript = (src) => {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error(`Script load error for ${src}`));
        document.head.appendChild(script);
    });
};

Promise.all([
    loadScript('../../utils/navTo.js?v=1.0'),
    loadScript('../../utils/utils.js?v=1.0')
])
.then(() => {
    document.getElementById('nav-bar').style.display = 'flex';
    
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
    } else {
        console.log("Access token found");
    }
})
.catch(error => console.error(error));
