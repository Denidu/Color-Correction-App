import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:video_player/video_player.dart';
import 'package:http_parser/http_parser.dart';

class CameraScreen extends StatefulWidget {
  final String selectedType;
  final String selectedSeverity;

  const CameraScreen({
    Key? key,
    required this.selectedType,
    required this.selectedSeverity,
  }) : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  File? mediaFile;
  String? processedMediaUrl;
  bool isVideo = false;
  bool isUploading = false; // Track upload status
  VideoPlayerController? _videoController; // For playing videos

  final ImagePicker _picker = ImagePicker();

  @override
  void dispose() {
    _videoController?.dispose();
    super.dispose();
  }

  // Capture Photo
  Future<void> _takePicture() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        mediaFile = File(pickedFile.path);
        isVideo = false;
        processedMediaUrl = null; // Reset processed URL
      });

      await _sendToBackend(mediaFile!, isVideo);
    }
  }

  // Record Video
  Future<void> _recordVideo() async {
    final pickedFile = await _picker.pickVideo(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        mediaFile = File(pickedFile.path);
        isVideo = true;
        processedMediaUrl = null; // Reset processed URL
      });

      _videoController?.dispose(); // Dispose the previous controller
      _videoController = VideoPlayerController.file(mediaFile!)
        ..initialize().then((_) {
          setState(() {});
          _videoController!.play();
        });

      await _sendToBackend(mediaFile!, isVideo);
    }
  }

  Future<void> _sendToBackend(File file, bool isVideo) async {
  setState(() {
    isUploading = true; // Show loading state
  });

  var request = http.MultipartRequest(
    'POST', Uri.parse('http://192.168.1.4:5000/upload'),
  );

  // Adding file data
  request.files.add(
    await http.MultipartFile.fromPath(
      isVideo ? 'video' : 'image', file.path,
      contentType: MediaType('multipart', 'form-data') // Ensure the correct content type
    ),
  );

  // Adding other fields
  request.fields['colorBlindnessType'] = widget.selectedType;
  request.fields['severity'] = widget.selectedSeverity;

  try {
    var response = await request.send();
    if (response.statusCode == 200) {
      var responseData = await response.stream.bytesToString();
      var jsonResponse = json.decode(responseData);

      setState(() {
        processedMediaUrl = jsonResponse["correctedMediaURL"];
      });
      print('Uploaded successfully!');
    } else {
      throw Exception('Upload failed: ${response.reasonPhrase}');
    }
  } catch (e) {
    print('Error: $e');
    setState(() {
      processedMediaUrl = null;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Upload failed: $e')),
    );
  } finally {
    setState(() {
      isUploading = false; // Stop loading state
    });
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
  appBar: AppBar(title: Text("Capture Media")),
  body: SingleChildScrollView(
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // Loading indicator when uploading
        if (isUploading) CircularProgressIndicator(),

        // Display Captured Image
        if (mediaFile != null && !isVideo)
          Image.file(mediaFile!, height: 300),

        // Display Captured Video
        if (mediaFile != null && isVideo && _videoController != null && _videoController!.value.isInitialized)
          AspectRatio(
            aspectRatio: _videoController!.value.aspectRatio,
            child: VideoPlayer(_videoController!),
          ),

        // Display Processed Media
        if (processedMediaUrl != null && processedMediaUrl!.isNotEmpty)
          isVideo
              ? Text("Processed Video URL: $processedMediaUrl")
              : Image.network(processedMediaUrl!,
                  errorBuilder: (context, error, stackTrace) {
                    return Text("Failed to load image.");
                  }),

        // Show loading spinner if no processed media
        if (processedMediaUrl == null || processedMediaUrl!.isEmpty)
          CircularProgressIndicator(),

        SizedBox(height: 20),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _takePicture,
              child: Text("Capture Photo"),
            ),
            SizedBox(width: 10),
            ElevatedButton(
              onPressed: _recordVideo,
              child: Text("Record Video"),
            ),
          ],
        ),
      ],
    ),
  ),
);

  }
}
