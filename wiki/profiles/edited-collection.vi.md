# Tuyển tập

**Mã hồ sơ:** `edited-collection`  
**Phù hợp nhất:** sách nhiều tác giả, sách biên soạn, tuyển tập kiểu kỷ yếu, và các sách nơi chương là đơn vị ấn phẩm với quan hệ người đóng góp và siêu dữ liệu riêng.

Hãy dùng hồ sơ khác với sách một tác giả, nơi siêu dữ liệu người đóng góp cấp chương chỉ thêm độ phức tạp không cần.

## Hồ sơ cho cảm giác gì

Trình bày học thuật hướng chương. Các đơn vị ấn phẩm có thể mang tiêu đề/phụ đề, tóm lược, từ khóa, định danh kiểu DOI và quan hệ người đóng góp, trong khi danh tính người đóng góp vẫn dùng lại được khắp cuốn sách.

Bộ trình diễn tích hợp của nó là `scholarly-collection`. Chế độ hệ thống trang là `book`, chế độ vật liệu bên là `fallback`, chế độ khảo chú là `available`, chế độ định vị là `none`, và chế độ văn bản song song là `none`.

## Mô-đun ngữ nghĩa

Mô-đun được bật bởi bản khởi đầu: `contributor-metadata`, `index`, `structural-hierarchy`, `publication-unit-metadata`.

Các mô-đun có chính sách tường minh cho hồ sơ này: `margin-objects`, `apparatus`.

| Mô-đun | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| `contributor-metadata` | bắt buộc | bật |
| `index` | khuyến nghị | bật |
| `structural-hierarchy` | bắt buộc | bật |
| `publication-unit-metadata` | bắt buộc | bật |
| `margin-objects` | tùy chọn | tắt |
| `apparatus` | tùy chọn | tắt |

`bắt buộc` nghĩa là hồ sơ phụ thuộc vào năng lực ngữ nghĩa ấy. `khuyến nghị`, `tùy chọn` và `không khuyến nghị` mô tả độ phù hợp biên tập; chúng không có nghĩa mọi tổ hợp về kỹ thuật khả thi đều đáng mong muốn.

## Bắt đầu từ các vùng dự án này

- khai báo đơn vị ấn phẩm — một đơn vị ngữ nghĩa mỗi chương hoặc mỗi bài đóng góp
- khai báo người đóng góp và quan hệ đóng góp — danh tính tách khỏi vai trò
- các tệp nội dung chương — nguồn bản thảo cho từng đơn vị
- `book.yml` — siêu dữ liệu cấp tập

Tạo một dự án khởi đầu riêng tư bằng:

```text
pse new /path/to/private-projects --profile edited-collection
```

Sau đó chạy:

```text
pse build .
pse check . --human
```

Đừng chỉnh các tệp được sinh trong `build/` như nguồn bản thảo, và đừng sửa lõi dùng chung của PSE để tùy biến một cuốn sách duy nhất.

## Các điểm tùy biến hữu ích

- Một người đóng góp có thể giữ vai trò khác nhau trong các đơn vị ấn phẩm khác nhau mà không phải nhân bản danh tính.
- Dùng tóm lược, từ khóa, định danh và ghi nhận người đóng góp cấp đơn vị ở trang mở chương.
- Khảo chú và vật thể lề tùy chọn vẫn sẵn dùng cho các tuyển tập chuyên biệt.

## Ranh giới và giới hạn

- Mô hình người đóng góp hiện hành là cục bộ và không tuyên bố đối chiếu danh tính ORCID/ROR bên ngoài.
- Nó không phải một hệ quản lý số tạp chí hay theo dõi bài gửi.

## Bản demo tổng hợp

Kho chứa một dự án nguồn tổng hợp và PDF hoàn thành dưới:

```text
examples/profiles/edited-collection/
```

Từ thư mục gốc kho PSE, tạo lại bản demo đó bằng:

```text
python scripts/examples/build_profile_demos.py edited-collection
```

Bản demo dùng để hiểu hồ sơ, không phải một bản mẫu bản thảo để chép mù. Hãy bắt đầu một cuốn sách thật bằng `pse new` để siêu dữ liệu dự án, kích hoạt mô-đun và cấu hình được sinh vẫn mạch lạc.

## Các trang cẩm nang liên quan

Quay lại [tổng quan hồ sơ](index.md), hoặc tiếp tục với [Tạo lập và kiểm tra PDF](../getting-started/build-and-check.md). Với các tính năng như khảo chú, vật thể lề, văn bản song song hay định vị, xem [Tính năng sách](../book-features/index.md).
