# Phân Loại Chủ Đề Văn Bản Tiếng Việt

## Mô tả dự án

Ứng dụng này được phát triển để phân loại chủ đề của văn bản tiếng Việt, phân loại nội dung thành 5 danh mục: Chính trị, Kinh tế, Văn hóa, Thể thao và Công nghệ. Dự án sử dụng mô hình học sâu `VinAI/phobert-base`, tận dụng framework PyTorch để xây dựng và huấn luyện mô hình, đồng thời triển khai trên nền tảng web với framework Django.

## Bắt đầu

Dữ liệu huấn luyện cho mô hình được thu thập từ các bài báo trên các trang báo điện tử uy tín như VnExpress và Thanh Niên. Phương pháp thu thập dữ liệu được mô tả chi tiết trong file script, với danh sách URL được lưu trong thư mục Collect_Urls. Sau khi thu thập, dữ liệu được tổng hợp và lưu trữ trong thư mục Raw_Data và được làm sạch tại thư mục Clean_Data, với các nhãn tương ứng cho từng chủ đề:

- **Chính trị**: Các bài viết liên quan đến chính sách, pháp luật, hoạt động của chính phủ.
- **Kinh tế**: Nội dung về thị trường, tài chính, doanh nghiệp.
- **Văn hóa**: Bài viết về lễ hội, nghệ thuật, phong tục.
- **Thể thao**: Tin tức về các sự kiện thể thao, trận đấu.
- **Công nghệ**: Các bài viết về công nghệ, AI, phần mềm.

Dữ liệu trong thư mục  được sử dụng để huấn luyện mô hình `VinAI/phobert-base`, trong khi một phần dữ liệu được tách ra để đánh giá hiệu suất của mô hình.

Dự án sử dụng thư viện PyTorch để xây dựng và huấn luyện mô hình. Để cài đặt PyTorch, vui lòng tham khảo hướng dẫn chi tiết tại trang web PyTorch.

## Yêu cầu

### Cài đặt PyTorch

Để cài đặt PyTorch, vui lòng tham khảo hướng dẫn chi tiết tại trang web PyTorch.

### Phiên bản Python

- 3.9 &lt;= Python &lt;= 3.11

## Hướng dẫn cài đặt

Clone repository:

```
https://github.com/moulsan369/VN_Topic_Classification.git
```

Tạo và kích hoạt môi trường ảo (khuyến nghị):

```
cd topic-classification
python -m venv venv
```

- Trên Windows:

```
venv\Scripts\activate
```

- Trên Linux:

```
source venv/bin/activate
```

Cài đặt các thư viện cần thiết:

```
pip install -r requirements.txt
```

Chạy dự án:

```
cd Django_Topic_Classification
python manage.py runserver
```

## Tài liệu phân tích

File tài liệu topic-classification.ipynb mô tả chi tiết các bước để xây dựng mô hình phân loại chủ đề văn bản tiếng Việt:

- Tiền xử lý dữ liệu
- Chuẩn hóa văn bản
- Huấn luyện mô hình với `VinAI/phobert-base`
- Phân loại chủ đề
- Đánh giá kết quả

## Hình ảnh giao diện

## Tài liệu tham khảo

- https://pytorch.org/docs/stable/index.html
- https://huggingface.co/VinAI/phobert-base
- https://www.analyticsvidhya.com/blog/2021/06/natural-language-processing-made-easy-using-huggingface/
- https://towardsdatascience.com/bert-for-nlp-tasks-an-introduction-to-transformers-5c5d1b7f7f
- https://medium.com/@datamonsters/text-classification-with-bert-and-transformers-a-full-guide-2b;
