let images = document.querySelectorAll('.carousel__photo');
images[0].classList.add("active");

document.querySelector('.carousel__button--next').addEventListener('click', () => {
    // alert('next');
    id = 0;
    for (let i = 0; i < images.length; i++) {
        if (images[i].classList.contains('active')) {
            if (i + 1 < images.length) {
                id = i + 1;
            } else
                id = 0;
            break;
        }
    }
    document.querySelector('.carousel__photo.active').classList.remove('active');
    images[id].classList.add('active');
});

document.querySelector('.carousel__button--prev').addEventListener('click', () => {
    id = images.length - 1;
    for (let i = images.length - 1; i >= 0; i--) {
        if (images[i].classList.contains('active')) {
            if (i - 1 >= 0) {
                id = i - 1;
            } else
                id = images.length - 1;
            break;
        }
    }
    document.querySelector('.carousel__photo.active').classList.remove('active');
    images[id].classList.add('active');
});