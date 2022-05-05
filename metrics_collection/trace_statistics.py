import json
from types import SimpleNamespace


def get_earliest_relative_time(longer_as_parent_spans):
    if len(longer_as_parent_spans):
        return min([(span, span["relativeStartTime"]) for span in longer_as_parent_spans], key=lambda x: x[1])[0]
    else:
        return None


def getLowestStartTime(allOverlay):
    temp = get_earliest_relative_time(allOverlay)
    if temp:
        result = {"duration": temp["duration"], "lowestStartTime": temp["relativeStartTime"]}
    else:
        result = {"duration": -1, "lowestStartTime": -1}
    return result


# Determines whether the cut spans belong together and then calculates the duration.
def getDuration(lowestStartTime, duration, allOverlay):
    durationChange = duration
    didDelete = False
    # print(len(allOverlay))
    for i in range(len(allOverlay)):
        if lowestStartTime + durationChange >= allOverlay[i]["relativeStartTime"]:
            if lowestStartTime + durationChange < allOverlay[i]["relativeStartTime"] + allOverlay[i]["duration"]:
                temp_duration = allOverlay[i]["relativeStartTime"] + allOverlay[i][
                    "duration"] - lowestStartTime + durationChange
                durationChange = temp_duration
            # print(json.dumps(allOverlay))
            allOverlay.pop(i)
            # print(json.dumps(allOverlay))
            didDelete = True
            break
    result = {"allOverlay": allOverlay, "duration": durationChange, "didDelete": didDelete}
    # print(json.dumps(result))
    return result


def onlyOverlay(allOverlay, allChildren, tempSelf, span):
    tempSelfChange = tempSelf
    duration = 0
    resultGetDuration = {"allOverlay": allOverlay, "duration": duration, "didDelete": False}
    # print(json.dumps(resultGetDuration))
    # print(json.dumps(resultGetDuration["allOverlay"]))
    # noOverlay = list(set(allChildren) - set(allOverlay))
    noOverlay = [i for i in allChildren if i not in allOverlay]
    lowestStartTime = 0
    totalDuration = 0
    result = getLowestStartTime(allOverlay)
    lowestStartTime = result["lowestStartTime"]
    duration = result["duration"]

    while True:
        resultGetDuration = getDuration(lowestStartTime, duration, resultGetDuration["allOverlay"])
        if (not resultGetDuration["didDelete"]) and (len(resultGetDuration["allOverlay"]) > 0):
            totalDuration = resultGetDuration["duration"]
            temp = getLowestStartTime(resultGetDuration["allOverlay"])
            lowestStartTime = temp["lowestStartTime"]
            duration = temp["duration"]
        if len(resultGetDuration["allOverlay"]) <= 0:
            break
    duration = resultGetDuration["duration"] + totalDuration
    # no cut is observed
    for i in range(len(noOverlay)):
        duration += noOverlay[i]["duration"]
    tempSelfChange += (span["duration"] - duration)
    return tempSelfChange


def calculate_content(span, all_spans, result_value=None):
    if result_value is None:
        result_value = {}
    result_value_change = result_value
    # print(result_value_change)

    # self time
    temp_self = 0
    longer_as_parent = False
    kinder_schneiden = False
    all_overlay = []
    longer_as_parent_span = []
    all_children = []
    for i in range(len(all_spans)):
        # i am a child?
        if span["spanID"] == all_spans[i]["spanID"]:
            continue
        if len(all_spans[i]["references"]) == 1:
            if span["spanID"] == all_spans[i]["references"][0]["spanID"]:
                all_children.append(all_spans[i])

    if len(all_children):
        # only one child
        if len(all_children) == 1:
            if span["relativeStartTime"] + span["duration"] >= all_children[0]["relativeStartTime"] + all_children[0][
                "duration"]:
                temp_self = span["duration"] - all_children[0]["duration"]
            else:
                temp_self = all_children[0]["relativeStartTime"] - span["relativeStartTime"]
        else:
            # is the child longer as parent
            for i in range(len(all_children)):
                if span["duration"] + span["relativeStartTime"] < all_children[i]["duration"] + all_children[i][
                    "relativeStartTime"]:
                    longer_as_parent = True
                    longer_as_parent_span.append(all_children[i])

            # do the children overlap
            for i in range(len(all_children)):
                for j in range(len(all_children)):
                    if all_children[i]["spanID"] != all_children[j]["spanID"]:
                        if (all_children[i]["relativeStartTime"] <= all_children[j]["relativeStartTime"]) and \
                                (all_children[i]["relativeStartTime"] + all_children[i]["duration"] >= all_children[j][
                                    "relativeStartTime"]):
                            kinder_schneiden = True
                            all_overlay.append(all_children[i])
                            all_overlay.append(all_children[j])
            # print(all_overlay)

            all_overlay = [i for n, i in enumerate(all_overlay) if i not in all_overlay[n + 1:]]
            # print(json.dumps(all_overlay))
            if (not longer_as_parent) and (not kinder_schneiden):
                temp_self = span["duration"]
                for i in range(len(all_children)):
                    temp_self -= all_children[i]["duration"]
            elif longer_as_parent and kinder_schneiden:
                xored_item = [a for a in all_overlay + longer_as_parent_span if
                              (a not in all_overlay) or (a not in longer_as_parent_span)]
                if not xored_item:
                    earliesetLongerAsParent = get_earliest_relative_time(longer_as_parent_span)
                    # remove all children who are longer as parent
                    all_children_without = [i for i in all_children if i not in longer_as_parent_span]
                    temp_self = earliesetLongerAsParent["relativeStartTime"] - span["relativeStartTime"]
                    for i in range(len(all_children_without)):
                        temp_self -= all_children_without[i]["duration"]

                else:
                    overlay_only = [i for i in all_overlay if i not in longer_as_parent_span]
                    all_children_without = [i for i in all_children if i not in longer_as_parent_span]
                    earliesetLongerAsParent = get_earliest_relative_time(longer_as_parent_span)

                    overlayWithout = []
                    for i in range(len(overlay_only)):
                        if not earliesetLongerAsParent["relativeStartTime"] <= overlay_only[i]["relativeStartTime"]:
                            overlayWithout.append(overlay_only[i])

                    for i in range(len(overlayWithout)):
                        if overlayWithout[i]["relativeStartTime"] + overlayWithout[i]["duration"] > \
                                earliesetLongerAsParent["relativeStartTime"]:
                            overlayWithout[i]["duration"] = overlayWithout[i]["relativeStartTime"] + overlayWithout[i][
                                "duration"] - earliesetLongerAsParent["relativeStartTime"]

                    temp_self = onlyOverlay(overlayWithout, all_children_without, temp_self, span)
                    diff = span["relativeStartTime"] + span["duration"] - earliesetLongerAsParent["relativeStartTime"]
                    temp_self -= diff

            elif longer_as_parent:
                temp_self = longer_as_parent_span[0]["relativeStartTime"] - span["relativeStartTime"]
                for i in range(len(all_children)):
                    if all_children[i]["spanID"] != longer_as_parent_span[0]["spanID"]:
                        temp_self -= all_children[i]["duration"]

            else:
                temp_self = onlyOverlay(all_overlay, all_children, temp_self, span)
    else:
        temp_self += span["duration"]
    # print(type(temp_self))
    if temp_self < 0:
        return result_value_change

    result_value_change["count"] += 1
    result_value_change["total"] += span["duration"]

    if result_value_change["min"] > span["duration"]:
        result_value_change["min"] = span["duration"]

    if result_value_change["max"] < span["duration"]:
        result_value_change["max"] = span["duration"]

    if result_value_change["selfMin"] > temp_self:
        result_value_change["selfMin"] = temp_self

    if result_value_change["selfMax"] < temp_self:
        result_value_change["selfMax"] = temp_self

    result_value_change["selfTotal"] += temp_self
    # print(result_value_change)
    return result_value_change
