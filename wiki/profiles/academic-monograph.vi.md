# Sách chuyên khảo

**Mã hồ sơ:** `academic-monograph`  
**Phù hợp nhất:** sách chuyên khảo nghiên cứu, luận văn được biên lại thành sách, và các lập luận học thuật kéo dài với hệ phân cấp chương thông thường.

Hãy dùng hồ sơ khác khi một vở kịch, tập thơ, ấn bản song ngữ đối chiếu, hoặc ấn bản khảo cứu nguồn có cấu trúc chính không phải chương văn xuôi thông thường.

## Hồ sơ cho cảm giác gì

Có cấu trúc và có chừng mực. Hệ phân cấp đánh số và ghi chú học thuật dễ soát, trong khi trang vẫn ít khảo chú hơn một hồ sơ ấn bản.

Bộ trình diễn tích hợp của nó là `scholarly-monograph`. Chế độ hệ thống trang là `asymmetric-scholarly`, chế độ vật liệu bên là `outer-margin`, chế độ khảo chú là `available`, chế độ định vị là `none`, và chế độ văn bản song song là `none`.

## Mô-đun ngữ nghĩa

Mô-đun được bật bởi bản khởi đầu: `index`, `structural-hierarchy`.

Các mô-đun có chính sách tường minh cho hồ sơ này: `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Mô-đun | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| `index` | khuyến nghị | bật |
| `structural-hierarchy` | bắt buộc | bật |
| `publication-unit-metadata` | khuyến nghị | tắt |
| `contributor-metadata` | khuyến nghị | tắt |
| `margin-objects` | khuyến nghị | tắt |
| `apparatus` | tùy chọn | tắt |

`bắt buộc` nghĩa là hồ sơ phụ thuộc vào năng lực ngữ nghĩa ấy. `khuyến nghị`, `tùy chọn` và `không khuyến nghị` mô tả độ phù hợp biên tập; chúng không có nghĩa mọi tổ hợp về kỹ thuật khả thi đều đáng mong muốn.

## Bắt đầu từ các vùng dự án này

- `content/chapter-01.tex` — thay chương tổng hợp bằng bản thảo của bạn
- `book.yml` — tên sách, tác giả, ngôn ngữ và năm xuất bản
- `config/semantic-modules.json` — chỉ kích hoạt các năng lực học thuật tùy chọn khi cần

Tạo một dự án khởi đầu riêng tư bằng:

```text
pse new /path/to/private-projects --profile academic-monograph
```

Sau đó chạy:

```text
pse build .
pse check . --human
```

Đừng chỉnh các tệp được sinh trong `build/` như nguồn bản thảo, và đừng sửa lõi dùng chung của PSE để tùy biến một cuốn sách duy nhất.

## Các điểm tùy biến hữu ích

- Dùng `config/pse-local.tex` cho các thay đổi thiết kế chữ hay khoảng cách cục bộ dự án thay vì sửa hồ sơ dùng chung.
- Thêm siêu dữ liệu đơn vị ấn bản khi từng chương cần tóm lược, từ khóa, định danh kiểu DOI, hoặc quan hệ người đóng góp.
- Chỉ kích hoạt khảo chú hoặc vật thể lề khi lập luận thực sự cần chúng.

## Ranh giới và giới hạn

- Hồ sơ không bật hệ định vị chuẩn nào. Nếu định vị nguồn ổn định là trung tâm, hãy bắt đầu từ một hồ sơ ấn bản.
- Nó giả định hệ phân cấp văn xuôi là cấu trúc tổ chức chính.

## Bản demo tổng hợp

Kho chứa một dự án nguồn tổng hợp và PDF hoàn thành dưới:

```text
examples/profiles/academic-monograph/
```

Từ thư mục gốc kho PSE, tạo lại bản demo đó bằng:

```text
python scripts/examples/build_profile_demos.py academic-monograph
```

Bản demo dùng để hiểu hồ sơ, không phải một bản mẫu bản thảo để chép mù. Hãy bắt đầu một cuốn sách thật bằng `pse new` để siêu dữ liệu dự án, kích hoạt mô-đun và cấu hình được sinh vẫn mạch lạc.

## Các trang cẩm nang liên quan

Quay lại [tổng quan hồ sơ](index.md), hoặc tiếp tục với [Tạo lập và kiểm tra PDF](../getting-started/build-and-check.md). Với các tính năng như khảo chú, vật thể lề, văn bản song song hay định vị, xem [Tính năng sách](../book-features/index.md).
