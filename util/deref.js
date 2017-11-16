/*******************************************************************************
 * @license
 * Copyright (c) 2014 Pivotal Software, Inc. and others.
 * All rights reserved. This program and the accompanying materials are made
 * available under the terms of the Eclipse Public License v1.0
 * (http://www.eclipse.org/legal/epl-v10.html), and the Eclipse Distribution
 * License v1.0 (http://www.eclipse.org/org/documents/edl-v10.html).
 *
 * Contributors:
 *     Pivotal Software, Inc. - initial API and implementation
*******************************************************************************/

/*global module*/

/**
 * Follow a 'trail' of properties starting at given object.
 * If one of the values on the trail is 'falsy' then
 * this value is returned instead of trying to keep following the
 * trail down.
 */
function deref(obj, props) {
	var it = obj;
	for (var i = 0; it && i < props.length; i++) {
		it = it[props[i]];
	}
	return it;
}

module.exports = deref;