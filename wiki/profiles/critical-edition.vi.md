# Ấn bản khảo cứu

**Mã hồ sơ:** `critical-edition`  
**Phù hợp nhất:** ấn bản khảo cứu hướng nguồn, ấn bản văn bản, và các ấn bản nơi định vị chuẩn, quyết định văn bản, dòng khảo chú và vật liệu học thuật giữ vai trò trung tâm.

Hãy dùng hồ sơ khác với sách chuyên khảo thông thường hoặc ấn bản hướng đọc, nơi khảo chú và định vị nguồn sẽ là gánh nặng biên tập không cần thiết.

## Hồ sơ cho cảm giác gì

Gọn và nghiêm về văn bản nguồn. Văn bản, định vị chuẩn hiển thị, khảo chú đa dòng, vật liệu học thuật, vật liệu đa ngôn ngữ và vật thể lề ngoài cùng tạo thành một hệ ấn bản tích hợp.

Bộ trình diễn tích hợp của nó là `source-critical`. Chế độ hệ thống trang là `asymmetric-scholarly`, chế độ vật liệu bên là `outer-margin`, chế độ khảo chú là `multi-stream`, chế độ định vị là `primary-visible`, và chế độ văn bản song song là `none`.

## Mô-đun ngữ nghĩa

Mô-đun được bật bởi bản khởi đầu: `canonical-locators`, `apparatus`, `multilingual`, `bibliography`, `index`, `scholarly-matter`, `structural-hierarchy`, `contributor-metadata`, `margin-objects`.

Các mô-đun có chính sách tường minh cho hồ sơ này: `publication-unit-metadata`.

| Mô-đun | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| `canonical-locators` | bắt buộc | bật |
| `apparatus` | bắt buộc | bật |
| `multilingual` | bắt buộc | bật |
| `bibliography` | bắt buộc | bật |
| `index` | khuyến nghị | bật |
| `scholarly-matter` | bắt buộc | bật |
| `structural-hierarchy` | khuyến nghị | bật |
| `publication-unit-metadata` | tùy chọn | tắt |
| `contributor-metadata` | bắt buộc | bật |
| `margin-objects` | khuyến nghị | bật |

`bắt buộc` nghĩa là hồ sơ phụ thuộc vào năng lực ngữ nghĩa ấy. `khuyến nghị`, `tùy chọn` và `không khuyến nghị` mô tả độ phù hợp biên tập; chúng không có nghĩa mọi tổ hợp về kỹ thuật khả thi đều đáng mong muốn.

## Bắt đầu từ các vùng dự án này

- `content/critical-text.tex` — văn bản đã biên tập và cấu trúc định vị ổn định
- `content/apparatus.tex` — các mục khảo chú nối với định vị ngữ nghĩa
- `content/editorial-notes.tex` — vật liệu giải thích/biên tập
- `references.bib` — nguồn thư mục
- `config/locator-scheme.json` và cấu hình định vị liên quan — chính sách định vị

Tạo một dự án khởi đầu riêng tư bằng:

```text
pse new /path/to/private-projects --profile critical-edition
```

Sau đó chạy:

```text
pse build .
pse check . --human
```

Đừng chỉnh các tệp được sinh trong `build/` như nguồn bản thảo, và đừng sửa lõi dùng chung của PSE để tùy biến một cuốn sách duy nhất.

## Các điểm tùy biến hữu ích

- Dùng các dòng khảo chú (`textual`, `editorial`, `translation`, `commentary`, `source`) theo chức năng biên tập, không theo nhãn thị giác.
- Dùng vật thể lề cho vật liệu thực sự hướng bên; hành vi fallback vẫn hiển thị khi không đặt được vào lề.
- Ghi đè thiết kế chữ và lưới ở mức cục bộ, nhưng giữ nguyên ID ngữ nghĩa ổn định.

## Ranh giới và giới hạn

- Hồ sơ này giả định quyền kiểm soát biên tập thực sự đối với một văn bản nguồn; nó cố tình nặng hơn một ấn bản hướng đọc.
- PSE không thiết lập tính hợp lệ học thuật của các cách đọc, bản chứng hay phán đoán biên tập.

## Bản demo tổng hợp

Kho chứa một dự án nguồn tổng hợp và PDF hoàn thành dưới:

```text
examples/profiles/critical-edition/
```

Từ thư mục gốc kho PSE, tạo lại bản demo đó bằng:

```text
python scripts/examples/build_profile_demos.py critical-edition
```

Bản demo dùng để hiểu hồ sơ, không phải một bản mẫu bản thảo để chép mù. Hãy bắt đầu một cuốn sách thật bằng `pse new` để siêu dữ liệu dự án, kích hoạt mô-đun và cấu hình được sinh vẫn mạch lạc.

## Các trang cẩm nang liên quan

Quay lại [tổng quan hồ sơ](index.md), hoặc tiếp tục với [Tạo lập và kiểm tra PDF](../getting-started/build-and-check.md). Với các tính năng như khảo chú, vật thể lề, văn bản song song hay định vị, xem [Tính năng sách](../book-features/index.md).

## Ấn bản học thuật có chú giải

Hồ sơ `critical-edition` cũng đáp ứng các ấn bản học thuật chú giải không thiết lập một văn bản ấn phê. Tên nó chỉ định một họ trình bày dùng lại được, **không** phải khẳng định rằng mọi đầu sách đều chứa ấn phê văn bản. Hãy chọn các mô-đun ngữ nghĩa bắt buộc và dòng khảo chú theo phương pháp biên tập được ghi nhận của ấn bản.
