export const insertIntoElement = (elementId, element) => {
    const el = document.getElementById(elementId);
    if (el)
        el.innerHTML = element;
}

export const appendToElement = (elementId, element) => {
    const el = document.getElementById(elementId);
    if (el)
        el.append(element);
}

export const toggleHidden = (elementId) => {
    const el = document.getElementById(elementId);
    if (el)
    {
        if (el.classList.contains("d-none")) {
            el.classList.remove('d-none');
            el.classList.add('block');
        }
        else {
            el.classList.add('d-none');
            el.classList.remove('block');
        }
    }
}