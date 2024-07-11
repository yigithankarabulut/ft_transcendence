import { navigateTo } from "../../utils/navTo.js";

const searchUrl = "http://127.0.0.1:8000/user/search";

export async function fetchUsers() {

    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
    } else {
        
        document.getElementById('search-form').addEventListener("submit", function(event) {
            event.preventDefault();
            document.getElementById("search-button").click();
        });

        document.getElementById("search-button").addEventListener("click", async () => {
            const searchValue = document.getElementById("search").value;
            const response = await fetch(searchUrl + "?page=1" + "&limit=5" +"&key=" + searchValue, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                }
            });

            const data = await response.json();
            const users = data[0].data;
            console.log(users);
            // const tableBody = document.querySelector('.widget-26 tbody');
            // tableBody.innerHTML = ''; // Clear previous content

            // tableBody = document.querySelector('.widget-26 tbody');

            // users.forEach(user => {
            //     const userElement = document.createElement('tr');
            //     userElement.innerHTML = `
            //         <td>
            //             <div class="widget-26-job-emp-img">
            //                 <img src="${user.avatar}" alt="Company" />
            //             </div>
            //         </td>
            //         <td>
            //             <div class="widget-26-job-title">
            //                 <a href="#">${user.job_title}</a>
            //                 <p class="m-0"><a href="#" class="employer-name">${user.employer_name}</a> <span class="text-muted time">${user.time}</span></p>
            //             </div>
            //         </td>
            //         <td>
            //             <div class="widget-26-job-info">
            //                 <p class="type m-0">${user.job_type}</p>
            //                 <p class="text-muted m-0">in <span class="location">${user.location}</span></p>
            //             </div>
            //         </td>
            //         <td>
            //             <div class="widget-26-job-salary">${user.salary}</div>
            //         </td>
            //         <td>
            //             <div class="widget-26-job-category bg-soft-danger">
            //                 <i class="indicator bg-danger"></i>
            //                 <span>${user.category}</span>
            //             </div>
            //         </td>
            //         <td>
            //             <div class="widget-26-job-starred">
            //                 <a href="#">
            //                     <svg
            //                         xmlns="http://www.w3.org/2000/svg"
            //                         width="24"
            //                         height="24"
            //                         viewBox="0 0 24 24"
            //                         fill="none"
            //                         stroke="currentColor"
            //                         stroke-width="2"
            //                         stroke-linecap="round"
            //                         stroke-linejoin="round"
            //                         class="feather feather-star"
            //                     >
            //                         <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            //                     </svg>
            //                 </a>
            //             </div>
            //         </td>
            //     `;
            //     tableBody.appendChild(userElement);
            // });
        }
        );
    }
}





