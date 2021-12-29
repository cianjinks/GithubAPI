if (!window.full_data_save) {
    window.full_data_save = JSON.parse(b.label)
}
var full_data = window.full_data_save
var new_data = { angle: [], color: [], contributions: [], index: [], login: []}
for (var i = 0; i < source.data.index.length; i++) {
    Object.keys(new_data).filter(key => key in full_data[this.value]).forEach(key => new_data[key].push(full_data[this.value][key][i]));
}
new_data.index = source.data.index

// Debug
console.log(source.data)
console.log(full_data[this.value])
console.log(new_data)

source.data = new_data
source.change.emit()