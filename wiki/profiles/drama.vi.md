# Kịch

**Mã hồ sơ:** `drama`  
**Phù hợp nhất:** kịch bản, văn bản kịch, script diễn xuất, và ấn bản học thuật/hướng đọc nơi nhân vật thoại, chỉ dẫn sân khấu, màn/cảnh và định vị dòng kịch đóng vai trò quan trọng.

Hãy dùng hồ sơ khác với văn xuôi hay thơ thông thường, nơi cấu trúc kịch sẽ là nhân tạo.

## Hồ sơ cho cảm giác gì

Nhận thức diễn xuất và định vị theo dòng. Nhãn nhân vật thoại, chỉ dẫn sân khấu, phân chia cấu trúc và định vị kịch có nhận thức trình bày, trong khi ngữ nghĩa của chúng độc lập với vị trí trang.

Bộ trình diễn tích hợp của nó là `dramatic-reading`. Chế độ hệ thống trang là `asymmetric-scholarly`, chế độ vật liệu bên là `outer-margin`, chế độ khảo chú là `available`, chế độ định vị là `primary-visible`, và chế độ văn bản song song là `none`.

## Mô-đun ngữ nghĩa

Mô-đun được bật bởi bản khởi đầu: `drama-structure`, `dramatic-locators`, `index`.

Các mô-đun có chính sách tường minh cho hồ sơ này: `structural-hierarchy`, `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Mô-đun | Chính sách | Mặc định khởi đầu |
| --- | --- | --- |
| `drama-structure` | bắt buộc | bật |
| `dramatic-locators` | bắt buộc | bật |
| `index` | khuyến nghị | bật |
| `structural-hierarchy` | không khuyến nghị | tắt |
| `publication-unit-metadata` | không khuyến nghị | tắt |
| `contributor-metadata` | khuyến nghị | tắt |
| `margin-objects` | khuyến nghị | tắt |
| `apparatus` | khuyến nghị | tắt |

`bắt buộc` nghĩa là hồ sơ phụ thuộc vào năng lực ngữ nghĩa ấy. `khuyến nghị`, `tùy chọn` và `không khuyến nghị` mô tả độ phù hợp biên tập; chúng không có nghĩa mọi tổ hợp về kỹ thuật khả thi đều đáng mong muốn.

## Bắt đầu từ các vùng dự án này

- nguồn nội dung kịch — nhân vật thoại, chỉ dẫn sân khấu, màn/cảnh và danh tính dòng
- `config/locator-orchestration.json` — chính sách định vị dòng kịch
- `book.yml` — siêu dữ liệu ấn phẩm

Tạo một dự án khởi đầu riêng tư bằng:

```text
pse new /path/to/private-projects --profile drama
```

Sau đó chạy:

```text
pse build .
pse check . --human
```

Đừng chỉnh các tệp được sinh trong `build/` như nguồn bản thảo, và đừng sửa lõi dùng chung của PSE để tùy biến một cuốn sách duy nhất.

## Các điểm tùy biến hữu ích

- Kích hoạt khảo chú khi cần can thiệp biên tập hoặc giải thích.
- Siêu dữ liệu người đóng góp sẵn dùng cho dịch giả, biên tập viên hoặc các vai trò khác.
- Dùng các ghi đè trình bày cục bộ dự án cho khoảng cách và cách hiển thị nhân vật thoại thay vì đổi lệnh ngữ nghĩa.

## Ranh giới và giới hạn

- Hệ phân cấp văn xuôi chung không được khuyến nghị theo mặc định vì cấu trúc kịch mới là áp đảo.
- Hồ sơ không mô hình hóa quản lý diễn tập, phần mềm bố trí sân khấu hay xin quyền diễn xuất.

## Bản demo tổng hợp

Kho chứa một dự án nguồn tổng hợp và PDF hoàn thành dưới:

```text
examples/profiles/drama/
```

Từ thư mục gốc kho PSE, tạo lại bản demo đó bằng:

```text
python scripts/examples/build_profile_demos.py drama
```

Bản demo dùng để hiểu hồ sơ, không phải một bản mẫu bản thảo để chép mù. Hãy bắt đầu một cuốn sách thật bằng `pse new` để siêu dữ liệu dự án, kích hoạt mô-đun và cấu hình được sinh vẫn mạch lạc.

## Các trang cẩm nang liên quan

Quay lại [tổng quan hồ sơ](index.md), hoặc tiếp tục với [Tạo lập và kiểm tra PDF](../getting-started/build-and-check.md). Với các tính năng như khảo chú, vật thể lề, văn bản song song hay định vị, xem [Tính năng sách](../book-features/index.md).
