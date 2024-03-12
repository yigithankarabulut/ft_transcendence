import { navigateTo, router } from "./src/utils/navTo.js";

// Tarayıcı geçmişindeki bir değişiklik olduğunda, yani kullanıcı geri ya da
// ileri butonlarına tıkladığında router fonksiyonunu tetikler. Bu, sayfanın
// dinamik olarak yeniden yüklenmesini ve doğru içeriğin gösterilmesini sağlar.
window.addEventListener("popstate", router);


// Rastgele bir favicon seçerek sayfa yüklenirken favicon'un değiştirilmesini sağlayan bir fonksiyon.
function generateFavIcon() {
    let links = ["public/images/42_Logo.svg.png"]
    let link = document.querySelector("link[rel~='icon']");
    let rand = Math.floor(Math.random() * 5);
    link.href = links[rand];
}
generateFavIcon();


//  HTML belgesi tamamen yüklendiğinde, yani DOM hazır olduğunda çalışacak olan bir olay dinleyicisi.
document.addEventListener("DOMContentLoaded", () => {
    // Sayfa üzerindeki tıklama olaylarını dinleyen bir olay dinleyicisi.
    // Bu olay dinleyicisi, sayfa üzerindeki bağlantılara tıklama olaylarını
    // izler ve navigateTo fonksiyonunu çağırarak sayfa yönlendirmesi gerçekleştirir.
    document.body.addEventListener("click", (e) => {
        if (e.target.matches("[data-nav]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }
    })
    router();
})
