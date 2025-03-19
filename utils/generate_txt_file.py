async def generate_txt_report(folder, number, data_dict):
    time = data_dict.get("time")
    image = data_dict.get("image", {})
    predictions = data_dict.get("predictions", [])
    image_width = image.get("width")
    image_height = image.get("height")
    types_count = max(predictions, key=lambda x: x.get('class_id')).get('class')

    report_lines = [
        f"Объект: {folder}",
        f"Отчет №{number}",
        f"Время: {time}",
        "Изображение:",
        f"   Ширина: {image_width}",
        f"   Высота: {image_height}",
        f"Количество распознанных элементов: {len(predictions)}",
        f"Количество распознанных типов элементов: {types_count}",
        "Прогнозы:",
        "   |-----------------------------|"
    ]

    for prediction in predictions:
        report_lines.append(f"   | Координата X: {prediction.get('x')}")
        report_lines.append(f"   | Координата Y: {prediction.get('y')}")
        report_lines.append(f"   | Ширина: {prediction.get('width')}")
        report_lines.append(f"   | Высота: {prediction.get('height')}")
        report_lines.append(f"   | Четкость распознавания: {int(round(prediction.get('confidence'), 2) * 100)}%")
        report_lines.append(f"   | Тип элемента: {prediction.get('class')}")
        report_lines.append("   |-----------------------------|")

    report_filename = f"./assets/Report_#{number}.txt"
    with open(report_filename, 'w', encoding='utf-8') as file:
        for line in report_lines:
            file.write(line + '\n')

    return report_filename
