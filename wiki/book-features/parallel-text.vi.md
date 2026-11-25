---
title: Văn bản song song
description: Giữ đối chiếu nguồn/đích ổn định khi chuyển giữa các chế độ trình bày song ngữ.
---

# Văn bản song song

Văn bản song song biểu diễn các đoạn nguồn và đích như các vật thể ngữ nghĩa ổn định, và nối chúng qua các quan hệ đối chiếu tường minh. PSE không suy đoán đối chiếu chỉ vì hai đoạn văn tình cờ nằm đối diện nhau trên một trang.

Một dự án song ngữ nhờ vậy có thể đổi trình bày mà không phải viết lại ID đoạn hay đối chiếu.

## Mô hình ngữ nghĩa

Mô-đun giữ các đoạn nguồn/đích, ID đối chiếu ổn định, định vị đối chiếu tùy chọn và ghi chú có kiểu. Khả năng tương thích ghi chú dịch được giữ lại cho các dự án cũ.

## Các chế độ trình bày

Hồ sơ Ấn bản song ngữ hỗ trợ năm chế độ trình bày trên cùng một nguồn ngữ nghĩa:

- `parallel-columns`;
- `facing-pages`;
- `sequential-blocks`;
- `source-dominant`;
- `target-dominant`.

Đổi chế độ không được viết lại `content/parallel.tex` hay biến vị trí trang/cột thành danh tính ngữ nghĩa.

## Chính sách hồ sơ

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | không khai báo | không áp dụng |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | bắt buộc | bật |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | không khai báo | không áp dụng |
| [Kịch](../profiles/drama.md) | không khai báo | không áp dụng |
| [Tuyển tập](../profiles/edited-collection.md) | không khai báo | không áp dụng |
| [Văn học](../profiles/literary-fiction.md) | không khai báo | không áp dụng |

Chỉ Ấn bản song ngữ hiện khai báo `parallel-text` là bắt buộc trong chính sách khởi đầu của nó. Việc vắng mặt khỏi chính sách hồ sơ khác không phải một tuyên bố không tương thích; nó nghĩa là PSE hiện không quảng bá mô-đun ấy như một phần của bề mặt chính sách khởi đầu được hỗ trợ của hồ sơ đó.

## Khi nào dùng

Dùng văn bản song song khi sự đối ứng giữa đơn vị nguồn và đích quan trọng về biên tập. Nếu bạn chỉ thỉnh thoảng trích dẫn một ngôn ngữ khác, hãy dùng văn bản đa ngôn ngữ thay vì xây một mô hình đối chiếu.

Về các hệ địa chỉ ổn định dùng bởi các đơn vị đã đối chiếu, xem [Định vị và địa chỉ ổn định](locators.md).
