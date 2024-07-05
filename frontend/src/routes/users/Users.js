import { navigateTo } from "../../utils/navTo.js";

const randomUserApiUrl = "https://randomuser.me/api/?results=20";

let currentPage = 1;
const usersPerPage = 4;
let users = [];

export async function fetchUsers() {

    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
    } else {
            const response = await fetch(randomUserApiUrl);
            if (!response.ok) {
                throw new Error("Failed to fetch random users");
            }
            const data = await response.json();
            users = data.results;
            displayUsers(users, currentPage);

        function displayUsers(users, page) {
            const usersList = document.getElementById('users-list');
            usersList.innerHTML = ''; // Clear previous content

            const startIndex = (page - 1) * usersPerPage;
            const endIndex = startIndex + usersPerPage;
            const usersToDisplay = users.slice(startIndex, endIndex);

            usersToDisplay.forEach(friend => {
                const friendCard = document.createElement('div');
                friendCard.className = 'col-md-4 mb-3';
                friendCard.innerHTML = `
                <div class="people-nearby">
                    <div class="nearby-user">
                        <div class="row">
                            <div class="col-md-2 col-sm-2">
                                <img src="${friend.picture.medium}" alt="user" class="profile-photo-lg">
                            </div>
                            <div class="col-md-7 col-sm-7">
                                <h5><a href="#" class="profile-link">${friend.name.first} ${friend.name.last}</a></h5>
                                <p>${friend.email}</p>
                                <p class="text-muted">${friend.location.city}, ${friend.location.country}</p>
                            </div>
                            <div class="col-md-3 col-sm-3">
                                <button class="btn btn-primary delete-btn pull-right add-friend-btn">Add Friend</button>
                            </div>
                        </div>
                    </div>
                </div>`;

                const addFriendButton = friendCard.querySelector('.add-friend-btn');
                addFriendButton.addEventListener('click', () => {
                    console.log('Friend information:', friend);
                    // İstediğiniz işlemleri burada yapabilirsiniz.
                });

                usersList.appendChild(friendCard);
            });

            displayPagination(users.length, page);
        }

        function displayPagination(totalUsers, page) {
            const paginationContainer = document.getElementById('pagination');
            paginationContainer.innerHTML = ''; // Clear previous content

            const totalPages = Math.ceil(totalUsers / usersPerPage);

            if (page > 1) {
                const prevButton = document.createElement('button');
                prevButton.className = 'btn btn-secondary';
                prevButton.innerText = 'Previous';
                prevButton.addEventListener('click', () => {
                    currentPage--;
                    displayUsers(users, currentPage);
                });
                paginationContainer.appendChild(prevButton);
            }

            if (page < totalPages) {
                const nextButton = document.createElement('button');
                nextButton.className = 'btn btn-secondary';
                nextButton.innerText = 'Next';
                nextButton.addEventListener('click', () => {
                    currentPage++;
                    displayUsers(users, currentPage);
                });
                paginationContainer.appendChild(nextButton);
            }
        }

    }
}
