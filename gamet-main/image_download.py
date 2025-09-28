from bing_image_downloader import downloader


def download_images(celebrity_name, num_images=10):

    print(f"Скачиваем изображения для {celebrity_name}...")
    downloader.download(celebrity_name, limit=num_images, output_dir='celebrity_photos', adult_filter_off=True,
                        force_replace=False, timeout=60)
    print(f"Изображения для {celebrity_name} успешно скачаны.")


celebrity_names = [
    "Dimash Kudaibergen",
    "Erkebulan Dairov",
    "Aidos Yerbosynuly",
    "Assel Sagatova",
    "Baurzhan Islamkhan",
    "Aliya Moldagulova",
    "Bibigul Tulegenova",
    "Ninety One band",
    "Kairat Nurtas",
    "Zhanar Dugalova",
    "Serik Sapiyev",
    "Gennady Golovkin",
    "Kanat Islam",
    "Olga Rypakova",
    "Aigul Imanbayeva",
    "Altynai Zhorabayeva",
    "Yerkebulan Daiyrov",
    "Aruzhan Jazilbekova",
    "Dinmukhamed Kunayev",
]


for celebrity_name in celebrity_names:
    try:
        download_images(celebrity_name, num_images=10)
    except Exception as e:
        print(f"Не удалось скачать изображения для {celebrity_name}. Ошибка: {e}")
