import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:video_player/video_player.dart';
import 'package:http_parser/http_parser.dart';
import 'media_preview_screen.dart';

class CameraScreen extends StatefulWidget {
  final String selectedColorBlindnessType;
  final String selectedColorBlindnessSeverity;

  const CameraScreen({
    Key? key,
    required this.selectedColorBlindnessType,
    required this.selectedColorBlindnessSeverity,
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

  Future<void> _takeSnapshots() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        mediaFile = File(pickedFile.path);
        isVideo = false;
      });

      await _sendMediaToServer(mediaFile!, isVideo);
    }
  }

  Future<void> _startRecordingVideo() async {
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

      await _sendMediaToServer(mediaFile!, isVideo);
    }
  }

  Future<void> _sendMediaToServer(File file, bool isVideo) async {
    setState(() {
      isUploading = true; 
    });

    var request = http.MultipartRequest(
      'POST', Uri.parse('https://5aa0-2402-4000-2150-235-eddd-559e-885-7957.ngrok-free.app/upload')
    );

    request.files.add(
      await http.MultipartFile.fromPath(
        isVideo ? 'video' : 'image', file.path,
        contentType: MediaType('multipart', 'form-data') 
      ),
    );

    request.fields['colorBlindnessType'] = widget.selectedColorBlindnessType;
    request.fields['severity'] = widget.selectedColorBlindnessSeverity;

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
                  onPressed: _takeSnapshots,
                  child: Text("Capture Photo"),
                ),
                SizedBox(width: 10),
                ElevatedButton(
                  onPressed: _startRecordingVideo,
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
