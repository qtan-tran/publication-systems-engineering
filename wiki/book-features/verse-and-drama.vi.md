---
title: Ngữ nghĩa thơ và kịch
description: Dùng cấu trúc ngữ nghĩa riêng cho thơ và văn kịch thay vì nhét chúng vào hệ phân cấp văn xuôi chung.
---

# Ngữ nghĩa thơ và kịch

Thơ và kịch thường cần cấu trúc ngữ nghĩa cụ thể hơn chương và các tiêu đề văn xuôi lồng nhau. Vì vậy PSE giữ cấu trúc thơ và kịch trong các mô-đun dùng lại chuyên biệt.

## Cấu trúc thơ

`verse-structure` sở hữu khổ thơ, các dòng thơ ngữ nghĩa và ID dòng thơ ổn định. Một dòng vật lý bị ngắt hiển thị **không phải** một dòng thơ ngữ nghĩa mới. Các nhãn hiển thị tùy chọn vẫn tách khỏi danh tính máy ổn định.

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | không khai báo | không áp dụng |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | không khai báo | không áp dụng |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | không khai báo | không áp dụng |
| [Kịch](../profiles/drama.md) | không khai báo | không áp dụng |
| [Tuyển tập](../profiles/edited-collection.md) | không khai báo | không áp dụng |
| [Văn học](../profiles/literary-fiction.md) | không khai báo | không áp dụng |

Không có hồ sơ trình bày thơ chuyên biệt. Mô-đun ngữ nghĩa `verse-structure` vẫn sẵn dùng, nhưng một đầu sách dùng nó cần một trình bày được soát xét tường minh.

## Cấu trúc kịch

`drama-structure` sở hữu nhân vật thoại, lời thoại, chỉ dẫn sân khấu, màn/cảnh và cấu trúc kịch liên quan.

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | không khai báo | không áp dụng |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | không khai báo | không áp dụng |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | không khai báo | không áp dụng |
| [Kịch](../profiles/drama.md) | bắt buộc | bật |
| [Tuyển tập](../profiles/edited-collection.md) | không khai báo | không áp dụng |
| [Văn học](../profiles/literary-fiction.md) | không khai báo | không áp dụng |

Hồ sơ Kịch yêu cầu và bật cấu trúc kịch. Nó cũng yêu cầu `dramatic-locators` để định vị dòng kịch ổn định:

| Hồ sơ | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| [Sách chuyên khảo](../profiles/academic-monograph.md) | không khai báo | không áp dụng |
| [Ấn bản song ngữ](../profiles/bilingual-edition.md) | không khai báo | không áp dụng |
| [Ấn bản khảo cứu](../profiles/critical-edition.md) | không khai báo | không áp dụng |
| [Kịch](../profiles/drama.md) | bắt buộc | bật |
| [Tuyển tập](../profiles/edited-collection.md) | không khai báo | không áp dụng |
| [Văn học](../profiles/literary-fiction.md) | không khai báo | không áp dụng |

## Sao không mô hình hóa những thứ này bằng tiêu đề?

Một dòng gợi nhân vật thoại không phải một tiêu đề mục; một chỉ dẫn sân khấu không phải một kiểu đoạn văn; một khổ thơ không đơn thuần là khối văn xuôi tách biệt về thị giác. Mã hóa các cấu trúc này theo ngữ nghĩa cho hệ QA và hệ trình bày có được thứ đáng tin cậy để làm việc.

Với kịch, dùng [hồ sơ Kịch](../profiles/drama.md). Với tác phẩm nặng thơ, dùng `verse-structure` với một trình bày cục bộ hoặc tùy biến được soát xét tường minh; đừng giả định `literary-fiction` cung cấp bố cục khổ thơ.
