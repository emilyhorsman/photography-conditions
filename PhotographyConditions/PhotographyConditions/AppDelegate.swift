//
//  AppDelegate.swift
//  PhotographyConditions
//
//  Created by Emily Horsman on 9/15/18.
//  Copyright © 2018 Emily Horsman. All rights reserved.
//

import Cocoa

@NSApplicationMain
class AppDelegate: NSObject, NSApplicationDelegate {

    @IBOutlet weak var menu: NSMenu!
    @IBOutlet weak var statusMenuItem: NSMenuItem!

    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)


    func applicationDidFinishLaunching(_ aNotification: Notification) {
        statusItem.button?.title = "☀"
        statusItem.menu = menu

        let url = URL(
            fileURLWithPath: NSHomeDirectory()
        ).appendingPathComponent(".photographyconditions")
        let authorization = try! String(contentsOf: url, encoding: .utf8)

        let qualityUrl = URL(string: "https://sunburst.sunsetwx.com/v1/quality?geo=43.2740851,-79.8994183")
        let task = URLSession.shared.dataTask(with: qualityUrl!) { (data, response, error) in
            guard let json = try? JSONSerialization.jsonObject(with: data!) as? [String: Any] else {
                print("Error!")
                NSApp.terminate(self)
                return
            }

            print(json?["features"]?[0]?["properties"]?["quality"])
        }
        task.resume()
    }

    func applicationWillTerminate(_ aNotification: Notification) {
        // Insert code here to tear down your application
    }


}

