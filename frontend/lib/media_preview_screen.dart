import 'dart:io';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:path_provider/path_provider.dart';
import 'package:dio/dio.dart';
import 'package:image_picker/image_picker.dart';
import 'package:flutter/services.dart';

class MediaPreviewScreen extends StatefulWidget {
  final String originalMediaPath;
  final String correctedMediaUrl;
  final bool isVideo;

  const MediaPreviewScreen({
    Key? key,
    required this.originalMediaPath,
    required this.correctedMediaUrl,
    required this.isVideo,
  }) : super(key: key);

  @override
  _MediaPreviewScreenState createState() => _MediaPreviewScreenState();
}

class _MediaPreviewScreenState extends State<MediaPreviewScreen> {
  VideoPlayerController? _originalController;
  VideoPlayerController? _correctedController;

  @override
  void initState() {
    super.initState();

    if (widget.isVideo) {
      _originalController = VideoPlayerController.file(File(widget.originalMediaPath))
        ..initialize().then((_) {
          setState(() {});
          _originalController!.play();
        }).catchError((e) {
          // Handle error loading original video
          print("Error loading original video: $e");
        });

      _correctedController = VideoPlayerController.network(widget.correctedMediaUrl)
        ..initialize().then((_) {
          setState(() {});
          _correctedController!.play();  // Make sure to start playing the corrected video
        }).catchError((e) {
          // Handle error loading corrected video
          print("Error loading corrected video: $e");
        });
    }
  }

  @override
  void dispose() {
    _originalController?.dispose();
    _correctedController?.dispose();
    super.dispose();
  }

  Future<void> _saveImage() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final path = '${directory.path}/corrected_image_${DateTime.now().millisecondsSinceEpoch}.jpg';

      final response = await Dio().get(
        widget.correctedMediaUrl,
        options: Options(responseType: ResponseType.bytes),
      );

      final file = File(path);
      await file.writeAsBytes(response.data);

      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Image saved to $path'),
      ));
    } on DioError catch (e) {
      print('Error saving image: $e');
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Failed to save image'),
      ));
    }
  }

  Future<void> _saveVideo() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final path = '${directory.path}/corrected_video_${DateTime.now().millisecondsSinceEpoch}.mp4';

      final response = await Dio().get(
        widget.correctedMediaUrl,
        options: Options(responseType: ResponseType.bytes),
      );

      final file = File(path);
      await file.writeAsBytes(response.data);

      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Video saved to $path'),
      ));
    } on DioError catch (e) {
      print('Error saving video: $e');
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Failed to save video'),
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Media Preview")),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  const Text("Captured Media",
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  widget.isVideo
                      ? (_originalController != null &&
                              _originalController!.value.isInitialized
                          ? AspectRatio(
                              aspectRatio: _originalController!.value.aspectRatio,
                              child: VideoPlayer(_originalController!),
                            )
                          : const CircularProgressIndicator())
                      : Image.file(File(widget.originalMediaPath),
                          fit: BoxFit.contain),
                ],
              ),
            ),
            const SizedBox(height: 20),
            Container(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  const Text("Corrected Media",
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  if (widget.isVideo)
                    (_correctedController != null &&
                            _correctedController!.value.isInitialized
                        ? AspectRatio(
                            aspectRatio: _correctedController!.value.aspectRatio,
                            child: VideoPlayer(_correctedController!),
                          )
                        : const CircularProgressIndicator())
                  else
                    Image.network(
                      widget.correctedMediaUrl,
                      fit: BoxFit.contain,
                    ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: widget.isVideo ? _saveVideo : _saveImage,
              child: const Text('Save Corrected Media'),
            ),
          ],
        ),
      ),
    );
  }
}
