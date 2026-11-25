# Văn học

**Mã hồ sơ:** `literary-fiction`  
**Phù hợp nhất:** tiểu thuyết, truyện vừa, tập truyện, và văn xuôi hướng trải nghiệm đọc nơi nhịp kể chuyện liên tục nên chiếm ưu thế trên trang.

Hãy dùng hồ sơ khác với các dự án cần hạ tầng học thuật hiển thị làm tầng đọc chính.

## Hồ sơ cho cảm giác gì

Im lặng và hướng trải nghiệm đọc. Các trang mở chương có chừng mực, chiều dài dòng được ưu tiên, và các cấu trúc học thuật chuyên biệt đứng ngoài dòng chảy đọc mặc định.

Bộ trình diễn tích hợp của nó là `fiction-reading`. Chế độ hệ thống trang là `book`, chế độ vật liệu bên là `fallback`, chế độ khảo chú là `deferred`, chế độ định vị là `none`, và chế độ văn bản song song là `none`.

## Mô-đun ngữ nghĩa

Mô-đun được bật bởi bản khởi đầu: không có.

Các mô-đun có chính sách tường minh cho hồ sơ này: `index`, `structural-hierarchy`, `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Mô-đun | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| `index` | không khuyến nghị | tắt |
| `structural-hierarchy` | không khuyến nghị | tắt |
| `publication-unit-metadata` | không khuyến nghị | tắt |
| `contributor-metadata` | tùy chọn | tắt |
| `margin-objects` | tùy chọn | tắt |
| `apparatus` | không khuyến nghị | tắt |

`bắt buộc` nghĩa là hồ sơ phụ thuộc vào năng lực ngữ nghĩa ấy. `khuyến nghị`, `tùy chọn` và `không khuyến nghị` mô tả độ phù hợp biên tập; chúng không có nghĩa mọi tổ hợp về kỹ thuật khả thi đều đáng mong muốn.

## Bắt đầu từ các vùng dự án này

- các tệp nội dung chương — nguồn tự sự
- `book.yml` — tên sách, tác giả, ngôn ngữ, năm xuất bản
- `config/pse-local.tex` — các điều chỉnh trình bày cục bộ dự án có chừng mực

Tạo một dự án khởi đầu riêng tư bằng:

```text
pse new /path/to/private-projects --profile literary-fiction
```

Sau đó chạy:

```text
pse build .
pse check . --human
```

Đừng chỉnh các tệp được sinh trong `build/` như nguồn bản thảo, và đừng sửa lõi dùng chung của PSE để tùy biến một cuốn sách duy nhất.

## Các điểm tùy biến hữu ích

- Dùng các ghi đè thiết kế chữ một cách tiết chế để hồ sơ giữ một nhịp đọc mạch lạc.
- Chú thích cuối trang và vật thể lề khả thi về kỹ thuật, nhưng cần được biện minh về biên tập.
- Siêu dữ liệu người đóng góp có thể được kích hoạt cho các trường hợp đặc biệt như dịch giả hoặc lời giới thiệu.

## Ranh giới và giới hạn

- Chỉ dẫn, phân cấp cấu trúc, siêu dữ liệu đơn vị ấn phẩm và khảo chú không được khuyến nghị theo mặc định.
- Đây không phải vật thay thế cho ngữ nghĩa cấp dòng của thơ, kịch hoặc ấn bản khảo cứu.

## Bản demo tổng hợp

Kho chứa một dự án nguồn tổng hợp và PDF hoàn thành dưới:

```text
examples/profiles/literary-fiction/
```

Từ thư mục gốc kho PSE, tạo lại bản demo đó bằng:

```text
python scripts/examples/build_profile_demos.py literary-fiction
```

Bản demo dùng để hiểu hồ sơ, không phải một bản mẫu bản thảo để chép mù. Hãy bắt đầu một cuốn sách thật bằng `pse new` để siêu dữ liệu dự án, kích hoạt mô-đun và cấu hình được sinh vẫn mạch lạc.

## Các trang cẩm nang liên quan

Quay lại [tổng quan hồ sơ](index.md), hoặc tiếp tục với [Tạo lập và kiểm tra PDF](../getting-started/build-and-check.md). Với các tính năng như khảo chú, vật thể lề, văn bản song song hay định vị, xem [Tính năng sách](../book-features/index.md).
