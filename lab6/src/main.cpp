#include <iostream>
#include <opencv2/opencv.hpp>

#include "CameraProvider.hpp"
#include "Display.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"
#include "MouseHandler.hpp"

int main() {
    const std::string windowName = "Lab 6";

    CameraProvider camera(0);
    if (!camera.isOpened()) {
        std::cerr << "Error: camera was not opened. Check that a webcam is connected and available.\n";
        return 1;
    }

    Display display(windowName);
    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;
    MouseHandler mouseHandler;

    int brightnessValue = frameProcessor.getBrightness();
    cv::createTrackbar("Brightness", windowName, &brightnessValue, 200,
                       FrameProcessor::onBrightnessTrackbar, &frameProcessor);
    cv::setMouseCallback(windowName, MouseHandler::callback, &mouseHandler);

    std::cout << "Controls:\n"
              << "  0 Normal\n"
              << "  1 Invert colors\n"
              << "  2 Gaussian blur\n"
              << "  3 Canny edge detector\n"
              << "  4 Sobel filter\n"
              << "  5 Binary threshold\n"
              << "  6 Quantization\n"
              << "  7 RGB glitch\n"
              << "  8 Picture in picture\n"
              << "  9 Draw rectangles with mouse\n"
              << "  A/D rotate, +/- zoom, mouse wheel zoom, I/J/K/L move frame, R reset\n"
              << "  Q or ESC quit\n";

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) {
            std::cerr << "Warning: empty frame received.\n";
            break;
        }

        int wheelDelta = mouseHandler.consumeWheelDelta();
        if (wheelDelta > 0) {
            keyProcessor.increaseZoom(0.1);
        } else if (wheelDelta < 0) {
            keyProcessor.decreaseZoom(0.1);
        }

        cv::Mat processed = frameProcessor.process(frame, keyProcessor.getMode(), keyProcessor, mouseHandler);
        display.show(processed);

        int key = cv::waitKey(1);
        if (!keyProcessor.processKey(key)) {
            break;
        }
    }

    cv::destroyAllWindows();
    return 0;
}
