let FormatFilterCon = document.getElementById("FormatFilterCon");
    let HighShoes = document.getElementById("HighShoes");
    let ShortShoes = document.getElementById("ShortShoes");
    let shebsheb = document.getElementById("shebsheb");
    let PriceFilterCon = document.getElementById("PriceFilterCon");
    let under = document.getElementById("under");
    let above = document.getElementById("above");
    let FilterConfirm = document.getElementById("FilterConfirm");
    let filterResult = []
    FilterConfirm.addEventListener("click", () => {
        filterResult = []
        console.log(proinfo[0][0]);
        if (document.getElementById("HighShoes").checked || document.getElementById("ShortShoes").checked || document.getElementById("shebsheb").checked) {
            for (let i = 0; i < ProId - 1; i++) {
                if (proinfo[i][0] === "h" && document.getElementById("HighShoes").checked == true) {
                    filterResult.push(`con${i + 1}`);
                }
                if (proinfo[i][0] == "n" && document.getElementById("ShortShoes").checked == true) {
                    filterResult.push(`con${i + 1}`);
                }
                if (proinfo[i][0] == "s" && document.getElementById("shebsheb").checked == true) {
                    filterResult.push(`con${i + 1}`);
                }
                document.getElementById(`con${i + 1}`).classList.add("disappear");


            }
            for (let i = 0; i < ProId - 1; i++) {
                if (document.getElementById("under").value != "" || document.getElementById("above").value != "") {
                    if (document.getElementById("under").value != "" && document.getElementById("above").value != "" && proinfo[i][2] <= document.getElementById("under").value && filterResult.includes(`con${i + 1}`) && proinfo[i][2] >= document.getElementById("above").value) {
                        document.getElementById(`con${i + 1}`).classList.remove("disappear");
                    }
                    else {
                        if (proinfo[i][2] <= document.getElementById("under").value && filterResult.includes(`con${i + 1}`) && document.getElementById("above").value == "") {
                            document.getElementById(`con${i + 1}`).classList.remove("disappear");
                        }
                        if (proinfo[i][2] >= document.getElementById("above").value && filterResult.includes(`con${i + 1}`) && document.getElementById("under").value == "") {
                            document.getElementById(`con${i + 1}`).classList.remove("disappear");
                        }
                    }
                }
                else
                    if (filterResult.length == 0) {
                        document.getElementById(`con${i + 1}`).classList.remove("disappear");
                    }
                    else
                        if (filterResult.includes(`con${i + 1}`)) {
                            document.getElementById(`con${i + 1}`).classList.remove("disappear");
                        }


            }
        }
        else
            if (document.getElementById("HighShoes").checked == false && document.getElementById("ShortShoes").checked == false && document.getElementById("shebsheb").checked == false && (document.getElementById("under").value != "" || document.getElementById("above").value != "")) {
                for (let i = 0; i < ProId - 1; i++) {
                    document.getElementById(`con${i + 1}`).classList.add("disappear");
                    if (document.getElementById("under").value != "" || document.getElementById("above").value != "") {
                        if (document.getElementById("under").value != "" && document.getElementById("above").value != "" && proinfo[i][2] <= document.getElementById("under").value && proinfo[i][2] >= document.getElementById("above").value) {
                            document.getElementById(`con${i + 1}`).classList.remove("disappear");
                        }
                        else {
                            if (proinfo[i][2] <= document.getElementById("under").value && document.getElementById("above").value == "") {
                                document.getElementById(`con${i + 1}`).classList.remove("disappear");
                            }
                            if (proinfo[i][2] >= document.getElementById("above").value && document.getElementById("under").value == "") {
                                document.getElementById(`con${i + 1}`).classList.remove("disappear");
                            }
                        }
                    }
                }

            }
            else
                if (document.getElementById("HighShoes").checked == false && document.getElementById("ShortShoes").checked == false && document.getElementById("shebsheb").checked == false && document.getElementById("under").value == "" && document.getElementById("above").value == "") {
                    for (let i = 0; i < ProId - 1; i++) {
                        document.getElementById(`con${i + 1}`).classList.remove("disappear");
                    }
                }

        console.log(filterResult)
        // console.log(pro[2][0])
    })