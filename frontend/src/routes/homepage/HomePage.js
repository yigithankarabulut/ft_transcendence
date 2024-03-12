from './HomePage.JS' import fetchUserDetails;

class HomePage {
    constructor(path) {
        this.path = path;
    }

    async render() {
        return fetch(this.path)
            .then(res => {
                if (!res.ok)
                    throw new Error("couldn't fetch route");
                return res.text();
            })
            .then(html => {
                fetchUserDetails();
                return html;
            });
    }
}

export default HomePage;
