async def get_defect(time_interval) -> tuple:
    """
    Преобразует вложенные списки для визуально удобного вида
    :return: tuple(list, int)
    """
    from update_quality_table import from_excel_table_quality
    values_quality_table = await from_excel_table_quality(time_interval=time_interval)

    end_list_quality_table = []
    count_defect = 0

    if not values_quality_table:
        return [], 0
    else:
        for value in values_quality_table:
            try:
                # для подсчета количества дефектов
                count_defect += int(value[12])
            except:
                pass
            local_list = [f"Дата проверки: {value[0]}\n",
                          f"*Дата производства*: {value[1]}\n",
                          f"_Наименование изделия_: {value[2]}\n",
                          f"*Фамилия*: {value[6]} | {value[7]}\n",
                          f"_Количество по сопроводительному_: {value[8]}\n",
                          f"Количество забракованных: {value[12]}\n",
                          f"_SAP-код изделия_: {value[14]}\n",
                          f"*Несоответствие сборщика*: {value[15]}\n",
                          f"_Кол-во брака оператора_: {value[16]}\n",
                          f"*Фамилия оператора*: {value[17]}\n",
                          f"_Несоответствия оператора_: {value[20]}\n",
                          f"_Фамилия контролера_: {value[21]}\n",
                          f"_Примечания_: {value[27]}\n\n"]
            end_list_quality_table.append(local_list)

    return end_list_quality_table, count_defect