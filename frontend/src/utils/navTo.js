import { routes } from "../Routes.js";

//  Bu fonksiyon, mevcut URL'ye göre uygun rotayı bulur ve rotanın bileşenini ve HTML dosyasını yükler.
// routes dizisini dolaşarak, URL'nin rotalardan biriyle eşleşip eşleşmediğini kontrol eder.
// Eşleşen rotayı bulur ve bu rotanın bileşenini ve HTML dosyasını yükler.
// HTML içeriğini root elementine yerleştirir.
// Eğer rotaya ait JavaScript dosyası varsa, dinamik olarak yükler.
export const router = async () => {
    const potentialMatches = routes.map(route => {
        return {
            route,
            isMatch: location.pathname === route.path
        }
    })
    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch)
    if (!match) {
        match = {
            route: routes[0],
            isMatch: true
        }
    }
    const root = document.getElementById('root');
    const component = new match.route.component(match.route.htmlPath);
    try {
        const html = await component.render();
        root.innerHTML = html;
        import(match.route.js);
    }
    catch(err) {
        console.log("there is an error");
    }
}


// Bu fonksiyon, belirli bir URL'ye geçişi yönetir. İşlevleri:
// history.pushState yöntemini kullanarak tarayıcı geçmişine yeni bir giriş ekler ve URL'yi günceller.
// router fonksiyonunu çağırarak sayfa yenileme işlemlerini başlatır.
export const navigateTo = (url) => {
    history.pushState(null, null, url);
    router();
}