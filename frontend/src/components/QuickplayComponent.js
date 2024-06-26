<<<<<<<< HEAD:frontend/src/components/QuickplayComponent.js
class QuickplayComponent {
    constructor(path) {
        this.path = path;
    }

========
class FriendsComponent {
    constructor(path) {
        this.path = path;
    }
>>>>>>>> 59b054ba26e225d7bf23f3293763f09b791dd1a7:frontend/src/components/FriendsComponent.js
    async render() {
        return fetch(this.path)
            .then(res => {
                if (!res.ok)
                    throw new Error("couldn't fetch route");
                return res.text();
<<<<<<<< HEAD:frontend/src/components/QuickplayComponent.js
            })
    }

}

export default QuickplayComponent;
========
            });
    }
}

export default FriendsComponent;
>>>>>>>> 59b054ba26e225d7bf23f3293763f09b791dd1a7:frontend/src/components/FriendsComponent.js
