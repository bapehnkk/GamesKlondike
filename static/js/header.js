// Search script
let searchInput = document.querySelector('.column__search-input');
let searchCross = document.querySelector('.column__search-cross');
let searchSearch = document.querySelector('.column__search-search');
searchInput.addEventListener('change', (event) => {
    if (searchInput.value != '' &&
        searchCross.classList.contains('hidden'))
        searchCross.classList.toggle('hidden');
    else {
        searchCross.classList.toggle('hidden');
        searchInput.value = '';
    }

});
searchCross.addEventListener('click', (event) => {
    searchCross.classList.toggle('hidden');
    searchInput.value = '';
});
searchSearch.addEventListener('click', (event) => {
    document.querySelector('.column__submit').click();
});

// Hide, show search input
document.querySelector('.small-search').addEventListener('click', (event) => {
    document.querySelectorAll('.column').forEach((element) => {
        element.classList.add('column-none');
    });
    document.querySelector('.column-ser').classList.remove('column-none');
    document.querySelector('.window').classList.remove('none');
});
let hideSer = () => {
    document.querySelector('.window').classList.add('none');
    document.querySelectorAll('.column').forEach((element) => {
        element.classList.remove('column-none');
        document.querySelector('.column-ser').classList.add('column-none');
    });

};
window.addEventListener('resize', (event) => {
    if (window.matchMedia("(min-width: 767px)").matches) {
        hideSer();
    }
});
document.querySelector('.window').addEventListener('click', (event) => {
    hideSer();
});

// Menu
document.querySelector('.menu__cross').addEventListener('click', (event) => {

    document.querySelector('.header .menu').classList.add('hide');
    setTimeout(() => {
        document.querySelector('.header .menu').classList.add('none');
        document.querySelector('.column__burger').classList.remove('active');
    }, 50);
});

document.querySelector('.column__burger').addEventListener('click', (event) => {
    if (document.querySelector('.column__burger').classList.contains('active')) {

        document.querySelector('.header .menu').classList.add('hide');
        setTimeout(() => {
            document.querySelector('.header .menu').classList.add('none');
            document.querySelector('.column__burger').classList.remove('active');
        }, 50);
    } else {

        document.querySelector('.header .menu').classList.remove('none');
        setTimeout(() => {
            document.querySelector('.header .menu').classList.remove('hide');
            document.querySelector('.column__burger').classList.add('active');
        }, 50);
    }
});
// Allerts
document.querySelector('.column__item.bell').addEventListener('click', (event) => {
    document.querySelector('.column__bell').classList.toggle('none');
    document.querySelector('.column__user').classList.add('none');
});

// User
document.querySelector('.column__item.user').addEventListener('click', (event) => {
    document.querySelector('.column__user').classList.toggle('none');
    document.querySelector('.column__bell').classList.add('none');
});

//all

document.querySelector('.main').addEventListener('click', (event) => {
    document.querySelector('.column__bell').classList.add('none');
    document.querySelector('.column__user').classList.add('none');

    document.querySelector('.header .menu').classList.add('hide');
    setTimeout(() => {
        document.querySelector('.header .menu').classList.add('none');
        document.querySelector('.column__burger').classList.remove('active');
    }, 100);
});