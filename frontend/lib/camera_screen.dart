import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:video_player/video_player.dart';
import 'package:http_parser/http_parser.dart';
import 'media_preview_screen.dart';

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
  bool isVideo = false;
  bool isUploading = false;
  VideoPlayerController? _videoController; 
  final ImagePicker _picker = ImagePicker();

  @override
  void dispose() {
    _videoController?.dispose();
    super.dispose();
  }

  Future<void> _takePicture() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        mediaFile = File(pickedFile.path);
        isVideo = false;
      });

      await _sendToBackend(mediaFile!, isVideo);
    }
  }

  Future<void> _recordVideo() async {
    final pickedFile = await _picker.pickVideo(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        mediaFile = File(pickedFile.path);
        isVideo = true;
      });

      _videoController?.dispose();
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
      isUploading = true; 
    });

    var request = http.MultipartRequest(
      'POST', Uri.parse('http://192.168.1.100:5002/upload'),
    );

    request.files.add(
      await http.MultipartFile.fromPath(
        isVideo ? 'video' : 'image', file.path,
        contentType: MediaType('multipart', 'form-data') 
      ),
    );

    request.fields['colorBlindnessType'] = widget.selectedType;
    request.fields['severity'] = widget.selectedSeverity;

    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        var responseData = await response.stream.bytesToString();
        var jsonResponse = json.decode(responseData);
        String correctedMediaUrl = jsonResponse["correctedMediaURL"];

        print('Uploaded successfully!');

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => MediaPreviewScreen(
              originalMediaPath: file.path,
              correctedMediaUrl: correctedMediaUrl,
              isVideo: isVideo,
            ),
          ),
        );
      } else {
        throw Exception('Upload failed: ${response.reasonPhrase}');
      }
    } catch (e) {
      print('Error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Upload failed: $e')),
      );
    } finally {
      setState(() {
        isUploading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Capture Media")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (isUploading) CircularProgressIndicator(),

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
