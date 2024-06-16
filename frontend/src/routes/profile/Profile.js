const userDetailUrl = "http://127.0.0.1:8000/user/details";
const updateUserUrl = "http://127.0.0.1:8000/user/update";

let originalUserData = {};

export async function fetchProfile() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        navigateTo("/login");
        return;
    }
    console.log("Fetching user details");
    try {
        const response = await fetch(userDetailUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            }
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }
        const data = await response.json();
        const user = data[0].data[0];
        console.log(user);

        // Update profile details
        document.getElementById("user-name").textContent = user.first_name;
        document.getElementById("user-location").textContent = user.last_name;
        document.getElementById("user-username").textContent = user.username;
        document.getElementById("user-phone").textContent = user.phone;
        document.getElementById("followers-count").textContent = 435;
        document.getElementById("projects-count").textContent = 10;
        document.getElementById("ranks-count").textContent = 73;

        // Save original user data
        originalUserData = { ...user };

    } catch (err) {
        console.error("Error fetching user details:", err.message);
    }
}

window.enableEditMode = function enableEditMode() {
    document.getElementById("user-name").classList.add("d-none");
    document.getElementById("user-location").classList.add("d-none");
    document.getElementById("user-username").classList.add("d-none");
    document.getElementById("user-phone").classList.add("d-none");

    document.getElementById("edit-first-name").classList.remove("d-none");
    document.getElementById("edit-last-name").classList.remove("d-none");
    document.getElementById("edit-username").classList.remove("d-none");
    document.getElementById("edit-phone").classList.remove("d-none");

    document.querySelector(".edit-buttons").style.display = "block";

    const firstName = document.getElementById("user-name").textContent;
    const lastName = document.getElementById("user-location").textContent;
    const username = document.getElementById("user-username").textContent;
    const phone = document.getElementById("user-phone").textContent;

    document.getElementById("edit-first-name").value = firstName;
    document.getElementById("edit-last-name").value = lastName;
    document.getElementById("edit-username").value = username;
    document.getElementById("edit-phone").value = phone;
}

window.cancelEdit = function cancelEdit() {
    document.getElementById("user-name").classList.remove("d-none");
    document.getElementById("user-location").classList.remove("d-none");
    document.getElementById("user-username").classList.remove("d-none");
    document.getElementById("user-phone").classList.remove("d-none");

    document.getElementById("edit-first-name").classList.add("d-none");
    document.getElementById("edit-last-name").classList.add("d-none");
    document.getElementById("edit-username").classList.add("d-none");
    document.getElementById("edit-phone").classList.add("d-none");

    document.querySelector(".edit-buttons").style.display = "none";
}

window.updateProfile = async function updateProfile() {
    const access_token = localStorage.getItem("access_token");
    const firstName = document.getElementById("edit-first-name").value;
    const lastName = document.getElementById("edit-last-name").value;
    const username = document.getElementById("edit-username").value;
    const phone = document.getElementById("edit-phone").value;
    const email = originalUserData.email; // Mevcut e-posta adresini kullan

    const updatedData = {
        first_name: firstName,
        last_name: lastName,
        username: username,
        phone: phone,
        email: email // E-posta adresini güncelleme isteğine ekle
    };

    try {
        const response = await fetch(updateUserUrl, {
            method: "PUT", // PUT isteği kullanıyoruz
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${access_token}`,
            },
            body: JSON.stringify(updatedData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error);
        }

        // Successfully updated, now reflect the changes
        document.getElementById("user-name").textContent = firstName;
        document.getElementById("user-location").textContent = lastName;
        document.getElementById("user-username").textContent = username;
        document.getElementById("user-phone").textContent = phone;

        cancelEdit();

    } catch (err) {
        console.error("Error updating user details:", err.message);
    }
}

document.addEventListener("DOMContentLoaded", fetchProfile);
