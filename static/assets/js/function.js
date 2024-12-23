// Pastikan text dan downloadImgText diinisialisasi
var text = "";
var downloadImgText = "";
var newData = [];

// Inisialisasi DataTable
var table = $("#datatable-results").DataTable();

// Format data agar sesuai dengan DataTable
function updateTable(data) {
  // Hapus data lama
  table.clear();

  // Tambahkan data baru
  table.rows.add(
    data.map((item) => {
      return [
        item.index, // Kolom No
        item.filename, // Kolom Filename
        item.predict, // Kolom Prediction
        // `<a href="${item.image_path}" target="_blank">View Image</a>` // Kolom Image Path
      ];
    })
  );

  // Refresh tampilan tabel
  table.draw();
}

$("#formPredict").submit(function (e) {
  e.preventDefault();

  var urlPred = $("#formPredict").attr("action");

  $.ajax({
    url: urlPred,
    type: "POST",
    data: new FormData(this),
    cache: false,
    processData: false,
    contentType: false,
    beforeSend: function () {
      // Tampilkan loading animation sebelum proses dimulai
      $("#loading").show();
    },
    success: function (data) {
      if (data["success"] == true) {
        var domDownload = document.getElementById("formDownload");
        var domResults = document.getElementById("statistik_result");
        var detection_results = data["detection_results"];
        detection_results.forEach((detect) => {
          newData.push({
            index: detect.index,
            filename: detect.filename,
            predict: detect.predict,
          });
          downloadImgText +=
            "<input name='img_results[]' type='hidden' value='" +
            detect.image_path +
            "'>";
        });
        updateTable(newData);

        downloadImgText += "<button style='margin-top: 10px; margin-bottom: 20px;' class='btn btn-success' type='submit'>Download Prediction Results</button>";

        text +=
          "<ul><li>Total Data: <span>" +
          data["n_images"] +
          "</span></li><li>Bacterial Spot: <span>" +
          data["bacterial_spot"] +
          "</span></li><li>Early Blight: <span>" +
          data["early_blight"] +
          "</span></li><li>Healthy: <span>" +
          data["healthy"] +
          "</span></li><li>Late Blight: <span>" +
          data["late_blight"] +
          "</span></li><li>Leaf Miner: <span>" +
          data["leaf_miner"] +
          "</span></li><li>Leaf Mold: <span>" +
          data["leaf_mold"] +
          "</span></li><li>Mosaic Virus: <span>" +
          data["mosaic_virus"] +
          "</span></li><li>Septoria Leaf Spot: <span>" +
          data["septoria"] +
          "</span></li><li>Spider Mites: <span>" +
          data["spider_mites"] +
          "</span></li><li>Yellow Leaf Curl Virus: <span>" +
          data["yellow_leaf_curl_virus"] +
          "</span></li><li>No Identity: <span>" +
          data["no_identity"] +
          "</span></li></ul>";

        domDownload.innerHTML = downloadImgText;
        domResults.innerHTML = text;

        swal("Berhasil!", "Proses Deteksi Berhasil!", "success");
      } else {
        swal("Error!", data["error"], "error");
      }
    },
    error: function (data) {
        swal("Error!", data, "error");
    },
    complete: function () {
      // Sembunyikan loading animation setelah respons diterima
      $("#loading").hide();
    },
  });
});
