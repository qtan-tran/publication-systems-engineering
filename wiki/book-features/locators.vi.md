---
title: Định vị và địa chỉ ổn định
description: Phối hợp các hệ định vị khác nhau mà không biến danh tính ngữ nghĩa của chúng thành số trang hay thành lẫn nhau.
---

# Định vị và địa chỉ ổn định

Một định vị là cách ổn định để chỉ tới một vị trí có nghĩa trong một ấn phẩm mà không phụ thuộc số trang PDF hiện hành. Các loại ấn bản khác nhau cần ngữ nghĩa định vị khác nhau, nên PSE giữ các động cơ của chúng tách riêng và phối hợp chúng qua một tầng chính sách chung.

Các không gian tên định vị hiện hành là:

- `canonical` — vị trí nguồn chuẩn do `canonical-locators` sở hữu;
- `dramatic-line` — địa chỉ dòng kịch do `dramatic-locators` sở hữu;
- `verse-line` — danh tính dòng thơ ổn định do `verse-structure` sở hữu;
- `parallel-alignment` — địa chỉ đơn vị đã đối chiếu do `parallel-text` sở hữu.

Sự phối hợp định vị chọn một không gian tên chính, các không gian tên phụ tùy chọn, cách đánh số hiển thị, và chính sách ID ổn định. Nó **không quy đổi** một loại định vị thành loại khác.

## Chính sách định vị chuẩn

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | không khai báo | không áp dụng |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | không khai báo | không áp dụng |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | bắt buộc | bật |
| [Kịch](../profiles/drama.md) | không khai báo | không áp dụng |
| [Tuyển tập](../profiles/edited-collection.md) | không khai báo | không áp dụng |
| [Văn học](../profiles/literary-fiction.md) | không khai báo | không áp dụng |

## Chính sách định vị kịch

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | không khai báo | không áp dụng |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | không khai báo | không áp dụng |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | không khai báo | không áp dụng |
| [Kịch](../profiles/drama.md) | bắt buộc | bật |
| [Tuyển tập](../profiles/edited-collection.md) | không khai báo | không áp dụng |
| [Văn học](../profiles/literary-fiction.md) | không khai báo | không áp dụng |

Các địa chỉ `verse-line` và `parallel-alignment` là năng lực của mô-đun sở hữu chúng chứ không phải các mục chính sách mô-đun riêng. Xem [Ngữ nghĩa thơ và kịch](verse-and-drama.md) và [Văn bản song song](parallel-text.md).

## ID ổn định và nhãn hiển thị

Một ID ngữ nghĩa ổn định và nhãn được in cho người đọc không phải là một. Một dòng thơ có thể giữ ID máy như `l17` trong khi hiển thị `17`, một nhãn khác do nguồn định nghĩa, hoặc không hiển thị nhãn nào. Vì thế một lần thiết kế lại không đòi viết lại không gian địa chỉ.

## Dùng định vị cho tham chiếu, đừng mượn phân trang

Nếu một ghi chú, tham chiếu chéo hay lập luận học thuật phải sống sót qua dàn lại và phân trang lại, hãy chỉ vào đơn vị ngữ nghĩa thay vì nhúng cứng số trang cuối vào logic bản thảo.
