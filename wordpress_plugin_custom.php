<?php
/*
Plugin Name: custom_3
Plugin URI: https://www.example.com/custom-news-plugin
Description: A custom WordPress plugin for fetching news from different sources and automatically posting them as blog posts.
Version: 1.0
Author: Your Name
Author URI: https://www.example.com
License: GPL2
*/
// Define constants
define('CNP_PLUGIN_DIR', plugin_dir_path(__FILE__));

// Hook activation and deactivation functions
register_activation_hook(__FILE__, 'cnp_activate');
register_deactivation_hook(__FILE__, 'cnp_deactivate');

// Activation callback
function cnp_activate() {
    // Perform activation tasks if needed
}

// Deactivation callback
function cnp_deactivate() {
    // Perform deactivation tasks if needed
}

// Hook the plugin code to run when WordPress is fully loaded
add_action('wp_loaded', 'cnp_plugin_code');

function cnp_plugin_code() {
    // Fetch data from different sources (e.g., websites, Telegram channels)
    // Store the fetched data in your custom database table
    // Implement the necessary data fetching logic based on your requirements

    // Create and schedule blog posts
    $data = cnp_get_data(); // Fetch data from your custom database table

    foreach ($data as $item) {
        // Format the post content
        $post_content = '<img src="https://picsum.photos/200">';
        // $post_content = '<img src="' . esc_url($item['image_url']) . '" alt="image loading failure">';
        $post_content .= '<p>' . esc_html($item['description']) . '</p>';

        // Prepare post data
        $post_data = array(
            'post_title'   => sanitize_text_field($item['title']),
            'post_content' => $post_content,
            'post_status'  => 'draft', // You can set the initial status as 'draft'
        );

        // Create the post
        $post_id = wp_insert_post($post_data);

        // Schedule the post to be published at a specific time
        $post_date = gmdate('Y-m-d H:i:s', strtotime('today 00:00:00')); // Adjust the time as needed
        wp_update_post(array(
            'ID'           => $post_id,
            'post_date'    => $post_date,
            'post_date_gmt'=> get_gmt_from_date($post_date),
            'post_status'  => 'future', // Change the status to 'publish' if you want the posts to be immediately published
        ));
    }
}

// Fetch data from the custom CSV file
function cnp_get_data() {
    $data = array();

    // Path to the CSV file
    $csv_file = plugin_dir_path(__FILE__) . 'telegram_data.csv';

    if (($handle = fopen($csv_file, 'r')) !== false) {
        // Skip the header row if it exists
        fgetcsv($handle);

        while (($row = fgetcsv($handle)) !== false) {
            $item = array(
                'title'       => $row[0], // Text from the 0th column
                'image_url'   => $row[3], // Image URL from the 3rd column
                'description' => $row[0],      // You can modify this based on your requirements
            );

            $data[] = $item;
        }

        fclose($handle);
    }

    return $data;
}

// Add your plugin settings page
// Implement the necessary functions to display and handle the plugin settings

// Add custom cron schedules for 00:00 and 12:00
add_filter('cron_schedules', 'cnp_custom_cron_schedules');

function cnp_custom_cron_schedules($schedules) {
    $schedules['twice_daily'] = array(
        'interval' => 43200, 
        'display'  => __('Twice Daily', 'custom-news-plugin'),
    );

    return $schedules;
}

// Schedule the automatic posts
register_activation_hook(__FILE__, 'cnp_schedule_posts');

function cnp_schedule_posts() {
    if (!wp_next_scheduled('cnp_publish_posts')) {
        wp_schedule_event(time(), 'twice_daily', 'cnp_publish_posts');
    }
}

// Hook the function to run when the scheduled event fires
add_action('cnp_publish_posts', 'cnp_publish_scheduled_posts');

function cnp_publish_scheduled_posts() {
    cnp_plugin_code(); // Call the plugin code to create and schedule the posts
}