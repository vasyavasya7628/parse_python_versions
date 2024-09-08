import openpyxl


def write_to_exel_output(filtered_list, filename):
    workbook = openpyxl.Workbook()
    print(filtered_list)
    worksheet = workbook.active

    for row_idx, row_data in enumerate(filtered_list, start=1):
        for col_idx, cell_value in enumerate(row_data, start=1):
            worksheet.cell(row=row_idx, column=col_idx, value=cell_value)

    workbook.save(f'{filename}.xlsx')
