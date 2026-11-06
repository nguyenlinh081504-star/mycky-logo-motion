# Công thức triển khai: nối pha sạch, xoay đúng và vẽ nét sắc

Đọc phần đúng triệu chứng; giữ concept/source đang chạy. Đây là bổ sung cho
[visual playbook](visual-playbook.md), không thay anatomy mapping hoặc artwork.
Code chạy được: [precision-motion.cjs](../scripts/precision-motion.cjs), dùng lại
`lesson-core.js`. Không cần cài package. Thử: `node scripts/test-precision-motion.cjs`.

| Triệu chứng / brief | Dùng phần |
|---|---|
| Ba clone +90° lần lượt, chữ béo giữ nguyên tới lúc ghép xong | A |
| Morph q=0 nhìn giống nhưng frame bắt đầu bị nháy | B |
| Đầu ribbon có móc thừa / thân bị khuyết | C |
| Vòng vẽ bị nấc, đầu bút xám hoặc hiện nét phía trước | D |
| Thu icon/wordmark giật từng pixel, lệch dấu tiếng Việt | E |
| Chỉ tăng tốc morph, sau đó toàn video 2× | F |

## A. Clone theo bản cha đã dừng, không quay lại từ góc 0

Áp dụng khi brief yêu cầu **ghép chữ gốc trước rồi mới morph**. Đây là thứ tự
khác với **morph xong mới clone**; không lấy một công thức làm mặc định mọi logo.

Tại đầu mỗi lượt, snapshot pose của bản cha đã dừng. Giữ pose cha bất biến.
Với trục màn hình x sang phải, y xuống dưới, góc dương quay theo kim đồng hồ:

`P_child(q) = C + R(90° E(q)) (P_parent_end − C)`

`angle_child(q) = angle_parent_end + 90° E(q)`

```js
const m = require('./scripts/precision-motion.cjs');
// Chỉ tạo snapshot một lần ở đầu lượt. Không đọc pose đang chạy mỗi frame.
const parentEnd = {x: 640, y: 700, angle: 90};
const pivot = [540, 800];
const childPose = m.quarterClone(parentEnd, pivot, easedProgress);
// q=0 trùng cha; q=1 đạt 180°. Lượt tiếp theo snapshot kết quả q=1 này.
```

Không tween x/y riêng sau phép quay. Chữ gốc angle=0 và mọi bản đã dừng không
xoay thêm. Bốn module còn nguyên hình dày trước khi phase morph được mở.
Kiểm các điểm q=0,.25,.5,.75,1: bán kính tâm module không đổi, cùng pivot,
endpoint 90°/180°/270°, không wrap, không yoyo. Đo tọa độ chưa đủ: xem giao nét.

## B. Endpoint chung có cùng coverage

1. Giữ nguyên source cubic qua entry, clone và morph; một renderer/fill rule/
   transform cho mọi phase. Không đổi từ raster source sang trace gần giống.
2. Ghép các section semantic trước. Cần tăng số đoạn thì **chia cubic source
   bằng de Casteljau**, không fit lại source theo knot của target.
   `subdivide(curve, n)` giữ đúng hình source. Target phải có cùng cấu trúc
   section; cùng số điểm tự nó không đảm bảo correspondence.
3. Tại boundary, render pose đóng băng và render morph với q=0 trên cùng canvas.
   So coverage chưa nén: số pixel đổi và max alpha error; phép chia có thể có sai
   số raster nhỏ nên đặt tolerance có căn cứ, không tự hạ ngưỡng để PASS.
   Xem tiếp frame đầu q>0: endpoint đúng chưa loại được đuôi nhọn/gợn ở giữa.
4. Nếu fitting độc lập gây khác subdivision giữa các clone, dùng chung local
   source template và cùng subdivision theo section; target khác nhau vẫn có
   thể giữ khác biệt thật của artwork. Không ép icon gần đối xứng thành đối xứng.
5. Khóa convention tọa độ: OpenCV contour thường biểu diễn tâm pixel, Cairo/SVG
   là tọa độ hình học. Với contour pixel-center, kiểm offset +0.5 khi đưa qua
   renderer; **không cộng 0.5 vô điều kiện** cho path vector có sẵn.
   Trace artwork ở độ phân giải gốc rồi áp transform; tránh trace lại bitmap
   đã scale/warp. Kiểm overlay native-size để quyết định convention.

## C. Strand ownership và tangent cục bộ

Tách đủ mỗi strand trước khi lồng: phần bị che cần phục dựng theo tiếp tuyến,
độ dày và reference, không bê nét của chữ kia. Khuyết ở cổ thường do seam từ
mask hợp thành; móc thừa ở đầu có thể do control handle quay ngược ở đoạn rất
ngắn. Debug màu từng strand ở nhiều q rồi xem lại màu thật.

Với cubic từ P0 đến P3, d=P3−P0: đo projection của P1−P0 và P3−P2 lên d/|d|.
Projection âm ở đoạn nhỏ cần kiểm vì có thể sinh loop. Chỉ sửa handle/section
đã chứng minh lỗi; không clamp tất cả handle vì sẽ phá hook, inflection hoặc
độ tương phản nét chủ đích. Mọi sửa phải giữ endpoint, shared junction và
width profile. Kiểm đoạn cong thực, self-intersection và frame đã decode.

Không cho hai strand trượt lồng trước lúc morph xong nếu brief khóa thứ tự đó.
Rút nét nối thừa là phase khác, có owner rõ; không ăn vào nét chính hay khoang âm.

## D. Draw-on liên tục, không feather rộng

Đã có `prefixCubic()` cho một cubic trong `lesson-core.js`; bản bổ sung hỗ trợ
cả chuỗi qua **một tổng chiều dài**:

```js
const table = m.arcTable(connectedCubics, 256); // tính một lần sau khi khóa path
const drawn = m.prefix(connectedCubics, table, easedProgress);
// Render các cubic hoàn tất + cubic cuối bị split, tuyệt đối không nối qua gap.
```

LUT xấp xỉ arc-length: tăng samples khi sai số pen-tip ở kích thước xuất vượt
tolerance; không gọi sampling cố định là tích phân chính xác. Clip prefix vào
silhouette artwork gốc nếu artwork có width profile, cap hoặc ornament riêng.
Không dùng stroke tròn rộng làm nét mới trong logo.

Nếu renderer raster đang có silhouette chính xác và đường dẫn đơn không tự
giao: precompute khoảng cách dọc đường của từng pixel bằng projection **lên
đoạn liên tục**, không timestamp theo vertex gần nhất.

`u = clamp(dot(X−A,B−A)/|B−A|²,0,1)`; `s_X = cumulative_i + u |B−A|`.

`projectArc(X,polyline)` minh họa này; không chạy vòng scan JS cho từng pixel HD
mỗi frame. Cache trường s_X hoặc vectorize trong renderer hiện có. Áp coverage
`m.coverage(s_X,L,q,1)` nhân silhouette; bề rộng 1 là **một pixel đầu ra**,
không phải feather 20px. Ở render 4× dùng width=4. q=0 trống, q=1 đủ nguyên
silhouette; phần overrun 1px bảo đảm không còn đuôi mờ ở endpoint.

**Giới hạn:** gần nhánh giao/đường chạy sát nhau, nearest projection có thể
chọn tương lai và làm lộ nét chưa tới. Phải gán branch/strand ownership hoặc
mask prefix riêng theo section; không áp nearest cho mọi logo. Kiểm pen front
phóng to, frame đầu/cuối và bước qua mỗi junction. Spatial coverage là chống
răng cưa, không phải fade toàn chữ để che morph lỗi.

## E. Dịch chuyển subpixel, giữ artwork và accent nguyên khối

Giữ float x/y đến rasterization. Với patch raster đặt tại (x,y): lấy
`ix=floor(x), iy=floor(y)`, warp patch theo `(x−ix,y−iy)` với padding, rồi đặt
tại ix,iy và clip theo **khung hình cuối**. Không round tọa độ từng frame.
Ảnh alpha dùng premultiplied alpha trước interpolation để tránh viền tối.
Artwork wordmark phải gồm cả dấu/descender; di chuyển cả cụm và downsample một
lần. Đừng tách chữ hoặc lộ từ trên xuống khi user yêu cầu hiện nguyên cụm.

Helper raster: `from precision_raster import place_rgba, coverage_difference`.
`place_rgba(canvas_rgba, artwork_rgba, x_float, y_float)` trả canvas mới, giữ
premultiplied alpha lúc warp; hỗ trợ entry âm ngoài màn hình. OpenCV nội suy
theo hệ số 1/32 pixel, nên dùng vector/higher resolution khi cần chặt hơn.
`coverage_difference(before_alpha, morph_q0_alpha)` đo số pixel đổi, max error
và sai diện tích trên alpha chưa nén; **không tự gán PASS**. Test chạy bằng
runtime đang có: `python scripts/test_precision_raster.py`.

Group icon bao gồm accent có cùng một matrix scale+translate. Cuối shrink
matrix khớp tọa độ artwork chính thức; không chuyển sang bitmap đích giữa chừng.
Tên chỉ hiện sau khi nhóm ổn định nếu brief yêu cầu. Nếu accent phải xuất hiện
nguyên hình một frame: gate theo frame index rõ, kiểm frame f−1/f/f+1; không
áp dụng grow/fade mặc định. Cơ chế accent do brief quyết định, không do skill.

## F. Time-map cục bộ rồi tăng tốc toàn phim

Chỉ sửa phase được yêu cầu; giữ entry/hold khác nếu user không sửa chúng.
Tối ưu hình học trước rồi chọn duration/easing; rút ngắn không chữa contour xấu.

```js
const revised = m.phaseMap({start:3.6,oldDuration:1.48,newDuration:1,
  totalDuration:8,policy:'extend-final-hold'});
const sourceTime = revised.at(outputTime);
// Phim vẫn 8s: morph 3.6–4.6; downstream sớm 0.48s; hold cuối dài hơn.
// Tăng toàn phim 2× sau đó: revised.at(2 * outputTime), duration=4s.
```

Chọn policy theo yêu cầu thật: `extend-final-hold` giữ tổng 8s bằng kéo hold
cuối đã hoàn thiện; `collapse` giảm tổng 8→7.52s, rồi 2× thành 3.76s.
Không âm thầm chọn policy làm đổi deliverable. Khi brief vẫn yêu cầu 8s, giữ
8s; khi đã yêu cầu toàn phim 2×, bản 8s thành 4s. 3.76s×60 không nguyên frame:
226 frame là 3.7667s, cần ghi đúng sai số lượng tử thời gian. Không tuyên bố
duration lẻ là chính xác nếu file đã làm tròn frame.

User chỉ nói 2× thì không thêm hold. User nói giữ logo cuối khoảng 1s thì
thay hold cũ theo frame hoàn thiện thực, tránh cộng chồng. Dùng `logo_lab retime`
đã có để xuất H.264/yuv420p/faststart; decode MP4 và kiểm tổng frame/duration.

## Nghiệm thu

Helper tests kiểm toán học, không cấp chứng nhận thẩm mỹ. Render đoạn khó với
renderer thật, xem q trung gian và frame sát mọi boundary; sau sửa mới xuất toàn
phim. Xem video ở tốc độ yêu cầu và frame decode toàn bộ. Nếu không thể phát
liên tục do công cụ/browser bị khóa, ghi rõ phần chưa kiểm, không suy ra PASS
1×/0.25× từ contact sheet. Giữ file QA nội bộ khi user chỉ muốn MP4.

Minh họa bổ sung: [ảnh](../assets/lessons/precision-refinements.png) ·
[video giáo dục](../assets/lessons/precision-refinements.mp4). Các hình tự dựng
không phải artwork hay bản QA của logo khách hàng.
Mở [precision lab](precision-lab.html) để tua tương tác; source hình và video
dùng chung `precision-lesson.cjs`. Không cần server hoặc package mới.
