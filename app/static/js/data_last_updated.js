function update_data_last_updated(record_created_at) {
    // A row of data is inserted into the `record` table at the end of the ELT process
    // Since we are using Canvas Data 2 as a data source, the Canvas data can be up to 
    // 4 hours old. This function will show the data last updated accounting for that lag time.

    // Check if the record has a valid date
    if (record_created_at) {
        const updatedDate = new Date(record_created_at + "Z");
        const displayDate = new Date(record_created_at + "Z");

        // console.log(updatedDate);

        // Subtract 4 hours to account for Canvas Data 2 lag
        displayDate.setUTCHours(displayDate.getUTCHours() - 4);

        const time_format = {
            timeZone: "America/Los_Angeles",
            year: "2-digit",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hour12: true // or false for 24-hour format
        };

        const formattedUpdatedDate = updatedDate.toLocaleString("en-US", time_format);
        const formattedDisplayDate = displayDate.toLocaleString("en-US", time_format);

        document.getElementById("data-last-updated").textContent = formattedDisplayDate;

        const tooltip_text = `The actual data update process last finished at ${formattedUpdatedDate}. ` +
            'However, the source for the Canvas data can be up to 4 hours old, which is why this time is shown.';

        // Initialize the tooltip and set the tooltip text
        $('#data-last-updated-tooltip').tooltip({
            title: tooltip_text,
            placement: 'bottom' // Adjust placement if needed
        });

    } else {
        // Handle the case where the record is null or has no last_updated field
        $('#data-last-updated-tooltip').tooltip({
            title: 'Data update time is unavailable',
            placement: 'bottom'
        });
    }
}
