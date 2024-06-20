// static/admin/js/wordimage_form.js
document.addEventListener('DOMContentLoaded', function() {
    const categoryField = document.querySelector('#id_category');
    const wordField = document.querySelector('#id_word');
    const dataList = document.createElement('datalist');
    dataList.id = 'word_list';
    wordField.parentNode.appendChild(dataList);

    categoryField.addEventListener('change', function() {
        const category = categoryField.value;
        fetch(`/admin/get_words_without_images/?category=${category}`)
            .then(response => response.json())
            .then(data => {
                while (dataList.options.length) {
                    dataList.remove(0);
                }
                data.words.forEach(word => {
                    const option = document.createElement('option');
                    option.value = word;
                    dataList.appendChild(option);
                });
            });
    });
});