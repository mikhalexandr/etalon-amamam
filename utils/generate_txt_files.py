import io

from core.settings import settings
from core.minio.access import get_minio_client


# Генерация текстовых отчетов
async def process_txt(
        object_id,
        name,
        reports_count,
        number,
        time,
        predictions_amount,
        types_amount,
        predictions,
        count_person_violations,
        count_construction_violations,
        count_person_with_helmet,
        count_person_without_helmet,
        count_person,
        filtered_boxes,
):
    report_lines = [
        f"Объект: {name}",
        f"Отчет №{reports_count}",
        f"Количество фото: {number}",
        f"Время: {time}",
        f"Количество распознанных элементов: {predictions_amount}",
        f"Количество распознанных типов элементов: {types_amount}",
        "Элементы объекта:",
    ]
    for key, value in predictions.items():
        report_lines.append(f" {key}:")
        report_lines.append("   |----------------------------------|")
        for prediction in value:
            report_lines.append(f"   | Координата X: {prediction.get('x')}")
            report_lines.append(f"   | Координата Y: {prediction.get('y')}")
            report_lines.append(f"   | Ширина: {prediction.get('width')}")
            report_lines.append(f"   | Высота: {prediction.get('height')}")
            report_lines.append(f"   | Четкость распознавания: {int(round(prediction.get('confidence'), 2) * 100)}%")
            report_lines.append(f"   | Тип элемента: {prediction.get('class')}")
            report_lines.append("   |----------------------------------|")

    report_text = "\n".join(report_lines)
    report_bytes = report_text.encode('utf-8')
    report_stream = io.BytesIO(report_bytes)
    object_name = f"{object_id}/{reports_count}/construction/Report_{reports_count}.txt"

    minio_client = await get_minio_client()
    async with minio_client as client:
        await client.put_object(
            Bucket=settings.minio_bucket,
            Key=object_name,
            Body=report_stream
        )

    report_lines = [
        f"Объект: {name}",
        f"Отчет №{reports_count}",
        f"Количество фото: {number}",
        f"Количество рабочих: {count_person}",
        f"Количество рабочих с правильной экипировкой: {count_person_with_helmet}",
        f"Количество рабочих с неправильной экипировкой: {count_person_without_helmet}",
        f"Количество нарушений со стороны персонала: {count_person_violations}",
        f"Количество нарушений на объекте: {count_construction_violations}",
        "Элементы объекта:",
    ]
    for key, value in filtered_boxes.items():
        report_lines.append(f" {key}:")
        report_lines.append("   |----------------------------------|")
        for prediction in value:
            report_lines.append(f"   | Координата X: {prediction.get('x')}")
            report_lines.append(f"   | Координата Y: {prediction.get('y')}")
            report_lines.append(f"   | Ширина: {prediction.get('width')}")
            report_lines.append(f"   | Высота: {prediction.get('height')}")
            report_lines.append(f"   | Четкость распознавания: {int(round(prediction.get('confidence'), 2) * 100)}%")
            report_lines.append(f"   | Тип элемента: {prediction.get('class')}")
            report_lines.append("   |----------------------------------|")

    report_text = "\n".join(report_lines)
    report_bytes = report_text.encode('utf-8')
    report_stream = io.BytesIO(report_bytes)
    object_name = f"{object_id}/{reports_count}/safety/Report_{reports_count}.txt"

    minio_client = await get_minio_client()
    async with minio_client as client:
        await client.put_object(
            Bucket=settings.minio_bucket,
            Key=object_name,
            Body=report_stream
        )
