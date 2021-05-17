function makeCSV() {
    return Promise.resolve($.get("https://vipsace.org/botapi/contacts?api_key=ANH$()U%$()EJRIJEWENITOIWORJWIEOUR()$URJWEJRIERKLEWNRJBEWR$")).then(data => {
        const rows = [ ['Phone NUm', 'name', 'email'].join(",") ];
        data.profiles.forEach(p => rows.push([p.phone_number, p.name, p.email].join(",")));
        return rows.join("\n")
    })
}

function postIds(ids) {
    return Promise.resolve(
        $.post("https://vipsace.org/botapi/contacts/stored?api_key=ANH$()U%$()EJRIJEWENITOIWORJWIEOUR()$URJWEJRIERKLEWNRJBEWR$", ids.map(id => "profile_id[]=" + id).join("&"))
    )
}


// postIds([192,193,194,195])
